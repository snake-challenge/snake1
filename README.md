# SNAKE #1

## Usage

### Local

1. Setup environment:
   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
   - TODO: setup Tensorflow and Jax with CUDA
   - TODO: `pip install snake1` ;)
2. Download and extract data:
   ```shell
   wget -nc https://microdata.epi.org/epi_cpsbasic.tar.gz
   mkdir epi_cpsbasic  
   tar -vxf epi_cpsbasic.tar.gz -C epi_cpsbasic --use-compress-program=pigz epi_cpsbasic_{2003..2021}.feather
   ```
3. Prepare data:
   ```shell
   snake1 prepare epi_cpsbasic/epi_cpsbasic_{2003..2021}.feather data.feather
   ```
   - Use with option `--seed <int>` for reproducibility. Refer to challenge guidelines below.
   - You can use `--n-jobs <int>` for parallel processing. Use -1 for all CPUs  
4. Create a task:
   ```shell
   snake1 task --synthesizer <synthesizer> --epsilon <epsilon> --background-frac <background> data.feather my_task/
   ```
   - Available synthesizers are: 
     - CopulaShirley
     - MST
     - PateGan
     - PrivBayes
   - Use option `--help` for usage information.
   - The following files will be created:
     - `my_task/background.csv`: background knowledge on train data
     - `my_task/synth.csv`: synthetic data
     - `my_task/targets.csv`: targets
     - `my_task/train.csv`: train data
     - `my_task/truth.csv`: targets true membership
5. Place your attack results in `my_task/attack.txt` with one guess (0 or 1) per line (for each target) and without header. 
    
    You can create a placeholder (random) attack with:
    ```shell
   shuf -r -i 0-1 -n <n_targets:100> > my_task/attack.txt
    ```
6. Score your attack:
   ```shell
   snake1 score my_task/truth.csv my_task/attack.txt
   ```

### Workflow

Work in progress ;)