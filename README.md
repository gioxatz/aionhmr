# Age-Inclusive 3D Human Mesh Recovery for Action-Preserving Data Anonymization

Official PyTorch implementation of the paper: **Age-Inclusive 3D Human Mesh Recovery for Action-Preserving Data Anonymization** 

Georgios Chatzichristodoulou, Niki Efthymiou, Panagiotis Filntisis, Georgios Pavlakos, Petros Maragos


[![arXiv](https://img.shields.io/badge/arXiv-2512.05259-B31B1B.svg)](https://arxiv.org/abs/2512.05259)


<img src="./assets/teaser.png">


## ✨ Highlights
- Age-inclusive 3D human mesh recovery framework
- Supports adults, children, and infants
- Designed for action-preserving anonymization
- Two complementary approaches:
  - AionHMR-a: Optimization-based
  - AionHMR-b: Transformer-based

---

## 📂 Project Structure

```bash
aionhmr/
 ├── aionhmr-a/        # Optimization-based method
 ├── aionhmr-b/        # Transformer-based method
 ├── assets/           
 ├── requirements.txt  # Core dependencies
 └── README.md
```
Each submodule contains its own ```README.md``` with detailed instructions.

---

## ⚙️ Installation


### 1. Clone the repository

```bash
git clone https://github.com/gioxatz/aionhmr.git
cd aionhmr
```

### 2. Create conda environment

```bash
conda create -n aionhmr_env python=3.10 -y
conda activate aionhmr_env
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install git+https://github.com/mattloper/chumpy --no-build-isolation
pip install git+https://github.com/facebookresearch/detectron2.git --no-build-isolation
pip install torch_scatter --no-build-isolation
```

⚠️ Note: detectron2 and torch_scatter are CUDA-dependent.
Please follow their official installation instructions if installation fails.

#### Dependencies for AionHMR-a
```bash
cd aionhmr-a
pip install phalp[all]@git+https://github.com/brjathu/PHALP.git --no-build-isolation
pip install -v -e third-party/ViTPose

cd third-party/DROID-SLAM
python setup.py install

pip install mmcv==1.3.9 --no-build-isolation
```

Ubuntu Version & CUDA Compatibility: This implementation was tested and developed with Ubuntu 20.04 and CUDA 12.4.

## 📄 Citation

If you find this work useful for your research, please consider citing our paper:
```bibtex
@misc{chatzichristodoulou2025ageinclusive3dhumanmesh,
  title={Age-Inclusive 3D Human Mesh Recovery for Action-Preserving Data Anonymization}, 
  author={Georgios Chatzichristodoulou and Niki Efthymiou and Panagiotis Filntisis and Georgios Pavlakos and Petros Maragos},
  year={2025},
  eprint={2512.05259},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2512.05259}, 
}
```

## 📜 License

This project is licensed under the MIT License. See LICENSE for details.

## 🙏 Acknowledgements

This work builds upon several excellent projects:

* [4DHumans](https://github.com/shubham-goel/4D-Humans)
* [SLAHMR](https://github.com/vye16/slahmr/)

We thank the authors for making their code publicly available.