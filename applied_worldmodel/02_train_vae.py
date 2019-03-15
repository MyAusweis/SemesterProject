#xvfb-run -a -s "-screen 0 1400x900x24" python3 02_train_vae.py --start_batch 0 --max_batch $(ls data | grep obs | wc -l) --new_model

from vae.arch import VAE
import argparse
import numpy as np
import config

def main(args):

    max_batch = args.max_batch
    new_model = args.new_model

    vae = VAE()

    if not new_model:
        try:
            vae.set_weights('./vae/weights.h5')
        except:
            print("Either set --new_model or ensure ./vae/weights.h5 exists")
            raise

    for batch_num in range(max_batch + 1):
        print('Building batch {}...'.format(batch_num))
        first_item = True

        for env_name in config.train_envs:
            try:
                new_data = np.load('./data/obs_data_' + env_name + '_' + str(batch_num) + '.npz')["arr_0"]
                if first_item:
                    data = new_data
                    first_item = False
                else:
                    data = np.concatenate([data, new_data])
                print('Found {}...current data size = {} episodes'.format(env_name, len(data)))
            except:
                pass

        if not first_item: # i.e. data has been found for this batch number
            data = np.array([item for obs in data for item in obs])
            vae.train(data)
        else:
            print('no data found for batch number {}'.format(batch_num))
            
    
    
    vae.train(max_batch)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Train VAE')
    parser.add_argument('--max_batch', type=int, default = 10, help='The max batch number') # --max_batch $(ls data | grep obs | wc -l)
    parser.add_argument('--new_model', action='store_true', help='start a new model from scratch?')
    args = parser.parse_args()

    main(args)
