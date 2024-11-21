# PROD 20241120_v0.10.12_src13_dec_min_1802_tuned

I need this production to analyse the LST-1 data of src13 (see https://www.lst1.iac.es/wiki/index.php/MC_analysis_and_IRF_production#lstmcpipe_productions) with dec -18.02 deg. The median of the NSB standard deviation for this dataset is approximately 1.940 p.e.

'''
lstmcpipe_generate_config PathConfigAllSkyFullDL1ab --dec_list dec_min_1802 --prod_id 20241120_v0.10.12_src13_dec_min_1802_tuned --kwargs source_prod_id=20241120_v0.10.12_src13_dec_min_1802_tuned
'''

Config for the NSB tuning:
 
"image_modifier": {
    "increase_nsb": true,
    "extra_noise_in_dim_pixels": 2.335,
    "extra_bias_in_dim_pixels": 0.785,
    "transition_charge": 8,
    "extra_noise_in_bright_pixels": 2.985
  }


Contact: Gaia V.
