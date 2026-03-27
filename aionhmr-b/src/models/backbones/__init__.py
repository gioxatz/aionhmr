from .vit import vit

def create_backbone(cfg):
    if cfg.MODEL.BACKBONE.TYPE == 'vit':
        return vit(cfg)#.to("cuda:1")
    else:
        raise NotImplementedError('Backbone type is not implemented')
