import torch
import torch.nn as nn
import torch.nn.functional as F

class ALU(torch.nn.Module):
    def __init__(self, model_dim=768, hidden_dim=512, internal_dim=10, use_output_projection=False):
        super(ALU, self).__init__()
        
        # input mlp does model_dim -> hidden_dim -> hidden_dim -> (internal_dim * 2 + 4) 
        self.input_mlp = nn.Sequential(
            nn.Linear(model_dim, hidden_dim),
            nn.LeakyReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LeakyReLU(),
            nn.Linear(hidden_dim, internal_dim * 2 + 4),
            nn.LeakyReLU()
        )
        
        if use_output_projection:
            # output projection does 1 -> internal_dim -> hidden_dim -> model_dim
            self.output_projection = nn.Sequential(
                nn.Linear(1, internal_dim),
                nn.ReLU(),
                nn.Linear(internal_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, model_dim)
            )

        self.eps = 1e-8
        self.base = torch.tensor([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])

    def forward(self, x):
        x = self.input_mlp(x)
        a = x[:, :10]
        b = x[:, 10:20]
        op = x[:, 20:24]
        
        base = torch.tensor([1, 2, 4, 8, 16, 32, 64, 128, 256, 512], device=x.device, dtype=x.dtype)
        a = torch.matmul(a, base)
        b = torch.matmul(b, base)
        
        op_weights = F.softmax(op, dim=1)  # Shape: (batch_size, 4)
        
        add = a + b
        sub = a - b
        mul = a * b
        div = a / (b + self.eps)
        
        op_outs = torch.stack([add, sub, mul, div], dim=1)  # Shape: (batch_size, 4)
        result = torch.sum(op_outs * op_weights, dim=1, keepdim=True)  # Shape: (batch_size, 1)
       
        if hasattr(self, 'output_projection'): 
            result = self.output_projection(result)
        
        return result



class ArithmeticAttentionModel(nn.Module):
    def __init__(self, model_dim=768, num_heads=8, num_layers=3):
        super(ArithmeticAttentionModel, self).__init__()
        
        # More robust input projection with multiple layers before normalization
        self.input_projection = nn.Sequential(
            nn.Linear(6, model_dim * 2),
            nn.ReLU(), 
            nn.Linear(model_dim * 2, model_dim),
            nn.LayerNorm(model_dim)
        )
        
        # self.pos_encoding = nn.Parameter(torch.randn(3, model_dim))
        
        self.attention_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=model_dim,
                nhead=num_heads,
                dim_feedforward=model_dim * 4,
                dropout=0.0,
                batch_first=True
            ) for _ in range(num_layers)
        ])
        
        self.alu = ALU(model_dim=model_dim)
        
        self.temp_linear = nn.Linear(model_dim, 1)
        
        self.apply(self._init_weights)
        
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
                
    def forward(self, num1, num2, operation):
        batch_size = num1.shape[0]
        
        x = torch.cat([num1, num2, operation], dim=1)
        
        x = self.input_projection(x)
        
        # x = x.view(batch_size, 3, -1)
        # x = x + self.pos_encoding.unsqueeze(0)
        
        for layer in self.attention_layers:
            x = layer(x)
        
        output = self.alu(x)
        
        # output = self.temp_linear(x)
        
        return output