import torch
import torch.nn as nn


class PatchEmbeding(nn.Module):
    def __init__(self, img_size: int, patch_size: int, in_chans: int = 3, embed_dim: int = 768):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2

        self.projection = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        x = self.projection(x)  # n_samples, embed_dim, n_patches ** 0.5 , n_patches ** 0.5
        # Wanted dimension n_samples, n_patches, embed_dim
        x = x.flatten(2)  # n_samples, embed_dim, n_patches
        x = x.transpose(1, 2)  # n_samples, n_patches, embed_dim
        return x


if __name__ == "__main__":
    x = torch.randn((1, 3, 64, 64))
    patch_embed = PatchEmbeding(img_size=64, patch_size=16)
    assert patch_embed(x).shape == (1, 16, 768)
