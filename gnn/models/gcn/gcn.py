from flax import linen as nn
from jax import numpy as jnp
from .gcn_layer import GCNLayer
from typing import Any

# GCN is a sequential model of GCN layers
class GCN(nn.Module):
    n_layers: int
    n_features: int

    def init_per_layer(self, params_per_layer: dict[str, Any]):
        return {
            "params": {f"GCNLayer_{i}": params_per_layer for i in range(self.n_layers)}
        }

    @nn.compact
    def __call__(self, node_features: jnp.ndarray, adj: jnp.ndarray):
        layers = [GCNLayer(self.n_features) for _ in range(self.n_layers)]
        for layer in layers:
            node_features, adj = layer(node_features, adj)
        return node_features
