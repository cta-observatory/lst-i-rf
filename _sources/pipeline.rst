==============================
Pipelines & configs generation
==============================

-----------------------
Prod3 & Prod5 pipelines
-----------------------

Here is the typical MC pipeline for the prod3 and prod5 productions

..
    All mermaid graph are commented here and images pointing to URLs. TO FIX.

..
    .. mermaid::

        flowchart LR
            subgraph R0
                gamma[R0 gamma]
                proton[R0 proton]
                electron[R0 electron]
            end

            gamma --> |r0_to_dl1| gamma_dl1[DL1 gamma]
            proton --> |r0_to_dl1| proton_dl1[DL1 proton]
            electron --> |r0_to_dl1| electron_dl1[DL1 electron]

            subgraph DL1
                direction LR
                gamma_dl1
                proton_dl1
                electron_dl1
            end


            subgraph DL1-test[DL1 test]
                direction LR
                gamma_dl1_test[DL1 gamma]
                proton_dl1_test[DL1 proton]
                electron_dl1_test[DL1 electron]
            end

            subgraph DL1-train[DL1 train]
                gamma_dl1_train[DL1 gamma]
                proton_dl1_train[DL1 proton]
            end


            gamma_dl1 --> train_test_split((train_test_split))
            proton_dl1 --> train_test_split
            train_test_split --> DL1-train
            train_test_split --> gamma_dl1_test & proton_dl1_test
            DL1-train --> train_pipe((train_pipe))
            train_pipe --> models
            models .-> real-data

            electron_dl1 --> electron_dl1_test

            subgraph DL2-test[DL2 test]
                direction LR
                gamma_dl2_test[DL2 gamma]
                proton_dl2_test[DL2 proton]
                electron_dl2_test[DL2 electron]
            end

            models --> DL2-test
            DL1-test --> DL2-test

            DL2-test --> |dl2_to_irf| IRF[IRFs]
            DL2-test --> |dl2_to_sensitivity| SENS[Sensitivity]
            SENS --> plot[png plots]

.. image:: https://mermaid.ink/img/pako:eNqdVV1rwjAU_SshD0NBh_row57cYOD2oI9tKZmNGkiTkqQbYv3vy4dN01YtW0C4vfec9Nx7LvYMdzzDcAmBPnvKf3ZHJBRYb2IGrkeWXweBiiPYzJqkOQeU5yjazFyQtIuF4IozU3VRp4wp3inhAHUcQDDLYtY82heA6fQFVGKWKp5mdF65rAmj1XreE-Fe2yO5tGf1xNViesS64KmB7BvD0oh2xxkRGk_0zeFwfXfm2lsT7OdDIb2J3VYyVVgqK9oEyZ-FpZ5_3-o27qHpbeiw_e1WBCLM9WKi5K5kjxvS7IH9ZegO1V9v18MybSOpLChRo1E3Mx53F_IuuQF2KxbuWx_AtT0DT113Grq_MZBTkALXXZg41N9kLSHX_xtUNmX3DJ51SWBEpxlSKBxdaL69oLcNdyxf1Nu7-N_2LlLPf7gJAW5oewPo8PZeB-NMdM10TDBGtcshYNEAKvtqnhKxr8D75i3SP5kMgCVmkijyTdSpAtvXz220bTIB2ZQssaBcRQU72EAmcAJzLHJEMv2ZOBt8DNUR5ziGSx1meI9KqmIYs4uGloU2Hr9mRHEBl3tEJZ5AVCq-PbEdXCpR4hq0Ikh7nNdJbDkf7nNkv0qXX-IaAyQ?type=png)](https://mermaid.live/edit#pako:eNqdVV1rwjAU_SshD0NBh_row57cYOD2oI9tKZmNGkiTkqQbYv3vy4dN01YtW0C4vfec9Nx7LvYMdzzDcAmBPnvKf3ZHJBRYb2IGrkeWXweBiiPYzJqkOQeU5yjazFyQtIuF4IozU3VRp4wp3inhAHUcQDDLYtY82heA6fQFVGKWKp5mdF65rAmj1XreE-Fe2yO5tGf1xNViesS64KmB7BvD0oh2xxkRGk_0zeFwfXfm2lsT7OdDIb2J3VYyVVgqK9oEyZ-FpZ5_3-o27qHpbeiw_e1WBCLM9WKi5K5kjxvS7IH9ZegO1V9v18MybSOpLChRo1E3Mx53F_IuuQF2KxbuWx_AtT0DT113Grq_MZBTkALXXZg41N9kLSHX_xtUNmX3DJ51SWBEpxlSKBxdaL69oLcNdyxf1Nu7-N_2LlLPf7gJAW5oewPo8PZeB-NMdM10TDBGtcshYNEAKvtqnhKxr8D75i3SP5kMgCVmkijyTdSpAtvXz220bTIB2ZQssaBcRQU72EAmcAJzLHJEMv2ZOBt8DNUR5ziGSx1meI9KqmIYs4uGloU2Hr9mRHEBl3tEJZ5AVCq-PbEdXCpR4hq0Ikh7nNdJbDkf7nNkv0qXX-IaAyQ


To generate a config for that pipeline, you may run:

.. code-block::

    lstmcpipe_generate_config PathConfigProd5Trans80 --prod_id whatagreatprod

**IMPORTANT NOTE:** prod5 MC files need the config to set "focal_length_choice": "EQUIVALENT" to be analyzed with ``lstchain >= v0.9``

In the lstchain config, please set:

.. code-block:: json

    "source_config": {
        "EventSource": {
            "focal_length_choice": "EQUIVALENT"
        }
    }


One can also start back from DL1, applying the dl1ab stage:

..
    .. mermaid::

        flowchart LR
            subgraph DL1a
                gamma[DL1 gamma]
                proton[DL1 proton]
                electron[DL1 electron]
            end

            gamma --> |dl1ab| gamma_dl1[DL1 gamma]
            proton --> |dl1ab| proton_dl1[DL1 proton]
            electron --> |dl1ab| electron_dl1[DL1 electron]

            subgraph DL1b
                direction LR
                gamma_dl1
                proton_dl1
                electron_dl1
            end


            subgraph DL1-test[DL1 test]
                direction LR
                gamma_dl1_test[DL1 gamma]
                proton_dl1_test[DL1 proton]
                electron_dl1_test[DL1 electron]
            end

            subgraph DL1-train[DL1 train]
                gamma_dl1_train[DL1 gamma]
                proton_dl1_train[DL1 proton]
            end


            gamma_dl1 --> train_test_split((train_test_split))
            proton_dl1 --> train_test_split
            train_test_split --> DL1-train
            train_test_split --> gamma_dl1_test & proton_dl1_test
            DL1-train --> train_pipe((train_pipe))
            train_pipe --> models
            models .-> real-data

            electron_dl1 --> electron_dl1_test

            subgraph DL2-test[DL2 test]
                direction LR
                gamma_dl2_test[DL2 gamma]
                proton_dl2_test[DL2 proton]
                electron_dl2_test[DL2 electron]
            end

            models --> DL2-test
            DL1-test --> DL2-test

            DL2-test --> |dl2_to_irf| IRF[IRFs]
            DL2-test --> |dl2_to_sensitivity| SENS[Sensitivity]
            SENS --> plot[png plots]

.. image:: https://mermaid.ink/img/pako:eNqVVMGKwjAQ_ZWQw6KgC_boYU-6sODuwR5tKbFNNZCmJU13Eeu_b5o0aVKt7BaE6Zs3M6_zYq4wLTMM1zCn5U96RlyA3T5iQD51czxxVJ3BZrdCGuqeEyoKdJCYjuIhU_FSlEyldOjkMMWp4H3WvPR5zLKI6VC1BMvlG2gzukLHViOJfLkbqWd4ZA1ZtqfCDPUKDGhLHGn3WzgO35MRLolEtjPrsvK7XuOl-Jg71VvB_cilwLVQyrog_rOAxNY9dsnnTNrl06Z98yVzRLTRKoofyrOcZ_osyXfSXZZtqXxVFUpwUleUiNlsjMzn7umZLNSkMaqo9hOfcHwfwMt467rUdnIkVKTCRnUXG70DosiF_NfSWqd0DF4lzDGiywwJZNbjGqkK75x9YGFgTl3wv1MXJLZu0lWH8-zUObTpU9d_uDZFi3YW2y3eT5lkMCRbNapMCM9b8LF_P8hfHT8h1pjVRJBvIi4tCLdf4SEckL6wg1VRRUtxqNhJBV1buIAF5gUimbxyrx07guKMCxzBtQwznKOGighG7CapTSWtxNuMiJLDdY5ojRcQNaIMLyyFa8EbbEgbgqR7hWVhVfSp73Z1xd9-AWAY62k?type=png)](https://mermaid.live/edit#pako:eNqVVMGKwjAQ_ZWQw6KgC_boYU-6sODuwR5tKbFNNZCmJU13Eeu_b5o0aVKt7BaE6Zs3M6_zYq4wLTMM1zCn5U96RlyA3T5iQD51czxxVJ3BZrdCGuqeEyoKdJCYjuIhU_FSlEyldOjkMMWp4H3WvPR5zLKI6VC1BMvlG2gzukLHViOJfLkbqWd4ZA1ZtqfCDPUKDGhLHGn3WzgO35MRLolEtjPrsvK7XuOl-Jg71VvB_cilwLVQyrog_rOAxNY9dsnnTNrl06Z98yVzRLTRKoofyrOcZ_osyXfSXZZtqXxVFUpwUleUiNlsjMzn7umZLNSkMaqo9hOfcHwfwMt467rUdnIkVKTCRnUXG70DosiF_NfSWqd0DF4lzDGiywwJZNbjGqkK75x9YGFgTl3wv1MXJLZu0lWH8-zUObTpU9d_uDZFi3YW2y3eT5lkMCRbNapMCM9b8LF_P8hfHT8h1pjVRJBvIi4tCLdf4SEckL6wg1VRRUtxqNhJBV1buIAF5gUimbxyrx07guKMCxzBtQwznKOGighG7CapTSWtxNuMiJLDdY5ojRcQNaIMLyyFa8EbbEgbgqR7hWVhVfSp73Z1xd9-AWAY62k

--------------------------
AllSky production pipeline
--------------------------

R0 to IRFs
==========

Standard AllSky production pipeline **for one training declination**

..
    .. mermaid::

        flowchart LR

            R0-Protons[R0 Protons \n - node a\n - node b\n - node c]
            R0-GammaDiffuse[R0 GammaDiffuse \n - node a\n - node b\n - node c]
            R0-GammaTest[R0 Gamma Test \n - node a\n - node b\n - node c]

            DL1-Protons[DL1 Protons \n - node a\n - node b\n - node c]
            DL1-GammaDiffuse[DL1 GammaDiffuse \n - node a\n - node b\n - node c]
            DL1-GammaTest[DL1 Gamma Test \n - node a\n - node b\n - node c]


            R0-GammaDiffuse --> |r0_to_dl1| DL1-GammaDiffuse
            R0-Protons --> |r0_to_dl1| DL1-Protons
            R0-GammaTest --> |r0_to_dl1| DL1-GammaTest


            DL1-GammaDiffuse --> |merge_dl1| DL1-GammaDiffuse-merged[DL1 Gamma Diffuse\nall nodes]
            DL1-Protons --> |merge_dl1| DL1-Protons-merged[DL1 Protons\nall nodes]

            DL1-GammaDiffuse-merged & DL1-Protons-merged --> train_pipe((train_pipe))

            train_pipe --> models .-> real_data[Real Data]

            models --> DL2-GammaTest

            DL1-GammaTest --> |merge_dl1| DL1-GammaTest-merged[DL1 Gamma Test \n - node a merged\n - node b merged\n - node c merged]
            DL1-GammaTest-merged ----> DL2-GammaTest
            DL2-GammaTest[DL2 Gamma Test \n - node a merged\n - node b merged\n - node c merged]

            DL2-GammaTest --> |dl2_to_irf| IRF-GammaTest
            IRF-GammaTest[IRF Gamma Test \n - node a merged\n - node b merged\n - node c merged]

.. image:: https://mermaid.ink/img/pako:eNqtVV1rgzAU_SshD6OFOloffdiT2xh0MNzemiJ3JrZCjCVGxmj735eoVTMjbN18Orkf5557c9UjTgrKcIBTXnwke5AKrSMiiEDtEy29F1moQpSbaIlaiIgO8JDQqQgG-H2Ak61F8gh5DmGWplXJDNPwfC3dGytVx4XM6adMPVe4XnUNanxth4bGatFw_aXHjrBusmP7ZZeTV4A87w6d5DJWRUz56jRqwLUBzqTW576d6TLGayv8rqDJzZncMbdEr_bRwXAu2okAzus5lFvnVTu5W9-Q9tKcTTituc1FNw7CuqaSkIn4kB3YbNbj-XxI2tvrlFxX5SW61VAy4DEFBZtIIxRqZMlpQ01WuPbtQTsXa3rGxjse8Gj7UBMyXMKxKWlNU-vdD8ihvM_wrRfC_y9JEyWa0VDum93NZHpCT9GDS5hl3ujTfwnDC6xxDhnV3-ejKUiw2rOcERxoSFkKFVcEE3HWodVBLwa7p5kqJA5S4CVbYKhU8fopEhwoWbFLUJjBTkLeRbE66bn5EdT_g_MXmSDsTg?type=png)](https://mermaid.live/edit#pako:eNqtVV1rgzAU_SshD6OFOloffdiT2xh0MNzemiJ3JrZCjCVGxmj735eoVTMjbN18Orkf5557c9UjTgrKcIBTXnwke5AKrSMiiEDtEy29F1moQpSbaIlaiIgO8JDQqQgG-H2Ak61F8gh5DmGWplXJDNPwfC3dGytVx4XM6adMPVe4XnUNanxth4bGatFw_aXHjrBusmP7ZZeTV4A87w6d5DJWRUz56jRqwLUBzqTW576d6TLGayv8rqDJzZncMbdEr_bRwXAu2okAzus5lFvnVTu5W9-Q9tKcTTituc1FNw7CuqaSkIn4kB3YbNbj-XxI2tvrlFxX5SW61VAy4DEFBZtIIxRqZMlpQ01WuPbtQTsXa3rGxjse8Gj7UBMyXMKxKWlNU-vdD8ihvM_wrRfC_y9JEyWa0VDum93NZHpCT9GDS5hl3ujTfwnDC6xxDhnV3-ejKUiw2rOcERxoSFkKFVcEE3HWodVBLwa7p5kqJA5S4CVbYKhU8fopEhwoWbFLUJjBTkLeRbE66bn5EdT_g_MXmSDsTg

To produce a config to run such a pipeline, typically run **on the cluster**:

.. code-block::

    lstmcpipe_generate_config PathConfigAllSkyFull --prod_id whatagreatprod --dec_list dec_2276


This will generate a lstmcpipe config file and a lstchain config file.

Please:
 * check thoroughly the lstmcpipe config
 * modify the lstchain config as you wish


DL1ab
=====

The DL1ab workflow is very similar, only starting from an existing DL1 dataset.

This workflow is typically used when a tuned production is needed for a given dataset.
For example, a production specifically tuned to match the Crab FoV NSB level and analyse Crab data.
In this case, you should produce your own lstchain config file using lstchain tools (see lstchain documentation).


..
    .. mermaid::

        flowchart LR

            DL1-Protons[DL1 Protons \n - node a\n - node b\n - node c]
            DL1-Protonsb[DL1 Protons tuned \n - node a\n - node b\n - node c]
            DL1-GammaDiffuse[DL1 GammaDiffuse \n - node a\n - node b\n - node c]
            DL1-GammaDiffuseb[DL1 GammaDiffuse tuned \n - node a\n - node b\n - node c]
            DL1-GammaTest[DL1 Gamma Test \n - node a\n - node b\n - node c]
            DL1-GammaTestb[DL1 Gamma Test tuned \n - node a\n - node b\n - node c]

            DL1-GammaDiffuse --> |dl1ab| DL1-GammaDiffuseb
            DL1-Protons --> |dl1ab| DL1-Protonsb
            DL1-GammaTest --> |r0_to_dl1| DL1-GammaTestb


            DL1-GammaDiffuseb --> |merge_dl1| DL1-GammaDiffuse-merged[DL1 Gamma Diffuse tuned\nall nodes]
            DL1-Protonsb --> |merge_dl1| DL1-Protons-merged[DL1 Protons tuned\nall nodes]

            DL1-GammaDiffuse-merged & DL1-Protons-merged --> train_pipe((train_pipe))

            train_pipe --> models .-> real-data

            models --> DL2-GammaTest

            DL1-GammaTestb --> |merge_dl1| DL1-GammaTest-merged[DL1 Gamma Test tuned \n - node a merged\n - node b merged\n - node c merged]
            DL1-GammaTest-merged ----> DL2-GammaTest
            DL2-GammaTest[DL2 Gamma Test \n - node a merged\n - node b merged\n - node c merged]

            DL2-GammaTest --> |dl2_to_irf| IRF-GammaTest
            IRF-GammaTest[IRF Gamma Test \n - node a merged\n - node b merged\n - node c merged]


.. image:: https://mermaid.ink/img/pako:eNqtVMtugzAQ_BXLhyqRQtVw5NATbVUplaq0t1BFCzaNJWMiY1RVIf9eY6A8bA5Jy2nZnR3PPuwTTnJCcYBTnn8lB5AKbbaRiATSX7hZe68yV7kodtpGrY0iHfaQ0IkIBnY8sJMPiyIecahSUHIp0xNkGYQsTcuCGrah4y9ksc12vcB3WqieD9W_V_PEU6KLZLmLRZ53jyrC1xBXdiesuVnwbp4OuQ1W3u1VvtcZ1aSYWtHMAJrMjMpPOslsEZ6JkUE_RpPSlQPnpvTCsXtO-jY4ZB6t54TTrbzNRjcOSnOqksDE_siOdLHo7eWyI-x9Bp7p03iBbrUpKXCPgIIO2sZqWLjx-8Za2ky351tah-1-zuwXaoDDNbNdSety7XDfDIfwBu2Pbo4_d3MuleKg77bZr1eUybRCz9vHqaCRa6f__ksQXmFtZ8CIfnJP9WERVgea0QgH2iQ0hZKrCEfirKHlUQ-fPhCmcomDFHhBVxhKlb99iwQHSpa0A4UMPiVkvyhqkl6at9088ecfuL_tWw?type=png)](https://mermaid.live/edit#pako:eNqtVMtugzAQ_BXLhyqRQtVw5NATbVUplaq0t1BFCzaNJWMiY1RVIf9eY6A8bA5Jy2nZnR3PPuwTTnJCcYBTnn8lB5AKbbaRiATSX7hZe68yV7kodtpGrY0iHfaQ0IkIBnY8sJMPiyIecahSUHIp0xNkGYQsTcuCGrah4y9ksc12vcB3WqieD9W_V_PEU6KLZLmLRZ53jyrC1xBXdiesuVnwbp4OuQ1W3u1VvtcZ1aSYWtHMAJrMjMpPOslsEZ6JkUE_RpPSlQPnpvTCsXtO-jY4ZB6t54TTrbzNRjcOSnOqksDE_siOdLHo7eWyI-x9Bp7p03iBbrUpKXCPgIIO2sZqWLjx-8Za2ky351tah-1-zuwXaoDDNbNdSety7XDfDIfwBu2Pbo4_d3MuleKg77bZr1eUybRCz9vHqaCRa6f__ksQXmFtZ8CIfnJP9WERVgea0QgH2iQ0hZKrCEfirKHlUQ-fPhCmcomDFHhBVxhKlb99iwQHSpa0A4UMPiVkvyhqkl6at9088ecfuL_tWw


The workflow then starts from a base production (the `source_prod_id`), produces new tuned DL1 (dl1ab steps) and trains a new set of models.

To prepare the lstmcpipe config, you want to:

- find a base production to start with (see the list of productions in the `documentation <productions>` and look for the latest "base" or "unuted" one) 
- run **on the cluster**:

.. code-block::

    lstmcpipe_generate_config PathConfigAllSkyFullDL1ab --dec_list dec_2276 --prod_id anothergreatprod --kwargs source_prod_id=whatagreatprod


Retrain and apply a model
=========================

..
    .. mermaid::

        flowchart LR

        subgraph pa[PROD A]
            direction TB
            gamma[DL1b merged gamma training]
            proton[DL1b merged proton training]
            gammaps[DL1b gamma testing\n- node 1\n- node  2\n...]
        end

        gamma & proton --> models

        %% DL1train --> train_pipe((train_pipe))

        models[models B] .-> real-data

        models & gammaps --> DL2-GammaTest[DL2 gamma testing\n- node 1\n- node  2\n...]


.. image:: https://mermaid.ink/img/pako:eNqVUstqwzAQ_BUhSEkgNsRHHwoNLr2ktKS5WaFsrI0jsB7IMqWE_HvXUkwa6KXyQePVzKxG0pk3ViIv-bGzX80JfGCbrTDCMBr9cGg9uBNzUL9v36rsaZ8WxiGVxyYoa9hufau2oDXU1WZ1YBp9izJVWPCgjDLtLwPnbbDmjptKf5Gji-sT-2qJfSCSECZjhkKw1Q2ygnCe51cHNHLKlLQPU6sse2SaFF0_EWYzRk3iFuJqRJ9OOZzPb3ixmPhJXaeJrfcsJ5FH6DIJAe5Z1PcaJFpXmyJ7Gf93FIWiFf9LNn58yensNChJd3geewkeTqhR8JKgxCMMXRBcmAtRB0d7wmepgvW8PELX45LDEOzHt2l4GfyAE6lSQHevpyJGzWt6K_HJXH4Ay4i5SA?type=png)](https://mermaid.live/edit#pako:eNqVUstqwzAQ_BUhSEkgNsRHHwoNLr2ktKS5WaFsrI0jsB7IMqWE_HvXUkwa6KXyQePVzKxG0pk3ViIv-bGzX80JfGCbrTDCMBr9cGg9uBNzUL9v36rsaZ8WxiGVxyYoa9hufau2oDXU1WZ1YBp9izJVWPCgjDLtLwPnbbDmjptKf5Gji-sT-2qJfSCSECZjhkKw1Q2ygnCe51cHNHLKlLQPU6sse2SaFF0_EWYzRk3iFuJqRJ9OOZzPb3ixmPhJXaeJrfcsJ5FH6DIJAe5Z1PcaJFpXmyJ7Gf93FIWiFf9LNn58yensNChJd3geewkeTqhR8JKgxCMMXRBcmAtRB0d7wmepgvW8PELX45LDEOzHt2l4GfyAE6lSQHevpyJGzWt6K_HJXH4Ay4i5SA

The workflow starts from an existing PROD A with merged DL1b datasets, trains a new set of models and applies them to create a new set of DL2.
**Note: In case of source-dependent analysis, the missing parameters are computed on the fly by lstchain, allowing the use of this PathConfig to not recreate DL1 files.**

Example of command to generate such a config:

.. code-block::

    lstmcpipe_generate_config PathConfigAllTrainTestDL1b --dec_list dec_2276 dec_931 --prod_id MY_NEW_PROD --kwargs source_prod_id=PROD-A


Using GammaDiffuse to produce full-enclosure IRFs
=================================================

The configs `PathConfigAllSkyTrainingWithSplit`, `PathConfigAllSkyTestingGammaDiffuse` and `PathConfigAllSkyFullSplitDiffuse` introduce the possibility to divide the GammaDiffuse dataset into training and testing datasets:

.. image:: https://mermaid.ink/img/pako:eNqdV9tq4zAQ_RUhaGkhCZbT5vawD0vYZaGFJZunbUJQbCU1-IassHGa_vsqll3XsseR6ydJ58zozIw0tt-wE7kMz_DOj_45r5QL9LRYhasQySc5bPecxq9oYfV_80hEYdJ3mUMUenlcjzNHeFGIlt_L1VC67POYvmQDuq4hW4Vs64ijECdHWOg2iflJg4DOvd3ukLAOivagoj2oaG-gaP5EvigJVAQKMtXTvV57SuD0EDg_xLxkS5YIIzFHbZ5q81OHYghOvdBoV8kEMiA4VA_Bv3JAhEEiXJ_I8yGN3NxISasrbCY2CG4mflV_P2B8z9zOYSgz82g-802C-szvEpt2OAu3ytFROTquQUaqGCnMOCnGyVTMcxbIS8Pa2jjpufo8KdeDqBDbYqkQtZDUpKlPo37_GzpzayOijfR4bmud2kun0bTe5T63Gng3VetCad6KFT1rF9kB3ySx74nzR28wIgO3VtkCoPR1cZZlVAltvzSacikC6Q4a81rUTIIoA1GOoiyOdcXntpPPiqnT0VQZ6_WsZ0VnVPYunUAboVvIQ6Y3y8Em9mJ2d1eO7-8LfeVaRg9krH6CBnLIGfU3LhX0ZSFHaC5H68Lq5qZgXozmT7bebHL0FrqzKg2ub1fA8ghUzvSFDOa-7B-1vlMKy_O2NHpB2fBRhwnbawQH7o_o1-JHZ50e37XrbCZsrxGctj5um3_x1GsLICmItHwPfWSsU6pqUjQkBZG6FD0-1R3k6qUvS-tzw7bQ3Wj9iNCuSq3JQrs2nAvcw3KLgHqu_Dd6uyytsHhlAVvhmRy6bEcPvljhVfguqfQgoj9p6OCZ4AfWw4dYdgM296gsQYBnO-oncjWm4d8oCgqSnOLZGz7iGSH2YDgcTh6mZPpo2RNCejiVy2MyGFnDkfUwehxJ0H7v4VPmwBqMp9ajPSZkPJ5Mh9PhqIeZ64mIP6u_ueyn7v0_3oNg4Q?type=png

.. 
    .. mermaid::

        flowchart LR

        subgraph R0-Protons-dec1[R0-$$p^+$$-dec1]
            direction TB
            node-rpa[node-a]
            node-rpb[node-b]
            node-rpc[node-c]
        end

        subgraph R0-GammaDiffuse-dec1[R0-$$\gamma$$-diffuse-dec1]
            direction TB
            node-rga[node-a]
            node-rgb[node-b]
            node-rgc[node-c]
        end

        subgraph DL1-GammaDiffuse-dec1[DL1-$$\gamma$$-diffuse-dec1]
            direction TB
            node-ga[node-a]
            node-gb[node-b]
            node-gc[node-c]
        end

        subgraph DL1-Protons-dec1[DL1-$$p^+$$-dec1]
            direction TB
            node-rga1[node-a]
            node-rgb1[node-b]
            node-rgc1[node-c]
        end

        subgraph R0-GammaTest[R0-$$\gamma$$-test]
            direction TB
            node-x
            node-y
            node-z
        end

        subgraph DL1-GammaDiffuse-train[DL1-$$\gamma$$-diffuse]
            direction TB
            node-tra[node-a]
            node-trb[node-b]
            node-trc[node-c]
        end

        subgraph DL1-GammaDiffuse-test[DL1-$$\gamma$$-diffuse]
            direction TB
            dl1-gammadiffuse-node-a[node-a]
            dl1-gammadiffuse-node-b[node-b]
            dl1-gammadiffuse-node-c[node-c]
        end

        subgraph DL1-GammaDiffuse-test-merged[DL1-$$\gamma$$-diffuse-merged]
            direction TB
            dl1-gammadiffuse-merged-node-a[node-a]
            dl1-gammadiffuse-merged-node-b[node-b]
            dl1-gammadiffuse-merged-node-c[node-c]
        end

        subgraph DL1-GammaTest[DL1-$$\gamma$$-test]
            dl1-gamma-node-x[node-x]
            dl1-gamma-node-y[node-y]
            dl1-gamma-node-z[node-z]
        end

        subgraph DL1-GammaTestMerged[DL1-GammaTestMerged]
            direction TB
            dl1-gamma-node-x-merged[node-x]
            dl1-gamma-node-y-merged[node-y]
            dl1-gamma-node-z-merged[node-z]
        end


        R0-GammaDiffuse-dec1 --> |r0_to_dl1| DL1-GammaDiffuse-dec1
        R0-Protons-dec1 --> |r0_to_dl1| DL1-Protons-dec1
        R0-GammaTest --> |r0_to_dl1| DL1-GammaTest


        node-ga --> |train-test_split| node-tra
        node-ga --> |train-test_split| dl1-gammadiffuse-node-a
        dl1-gammadiffuse-node-a ---> |merge_dl1| dl1-gammadiffuse-merged-node-a


        node-tra --> |merge_dl1| DL1-GammaDiffuse-dec1-merged[DL1-$$\gamma$$-diffuse train]
        node-trb --> |merge_dl1| DL1-GammaDiffuse-dec1-merged
        node-trc --> |merge_dl1| DL1-GammaDiffuse-dec1-merged

        DL1-Protons-dec1 ---> |merge_dl1| DL1-Protons-dec1-merged[DL1-$$p^+$$-dec1]
        
        DL1-GammaDiffuse-dec1-merged & DL1-Protons-dec1-merged --> train_pipe((train_pipe))

        train_pipe --> models .-> real_data[Real Data]

        %% models --> DL2-GammaTest
        models & dl1-gamma-node-x-merged ---> |dl1_to_dl2| dl2-gamma-node-x


        DL1-GammaTest -----> |merge_dl1| DL1-GammaTestMerged

        subgraph  DL2-GammaDiffuseTest
            direction TB
            dl2-gammadiffuse-node-a
            dl2-gammadiffuse-node-b
            dl2-gammadiffuse-node-c
        end

        subgraph  IRF-GammaDiffuseTest
            direction TB
            irf-gammadiffuse-node-a
            irf-gammadiffuse-node-b
            irf-gammadiffuse-node-c
        end

        subgraph DL2-GammaTest
            direction TB
            dl2-gamma-node-x
            dl2-gamma-node-y
            dl2-gamma-node-z
        end

        subgraph IRF-GammaTest
            direction TB
            irf-gamma-node-x
            irf-gamma-node-y
            irf-gamma-node-z
        end

        dl2-gamma-node-x --> |dl2_to_irf| irf-gamma-node-x

        models & dl1-gammadiffuse-merged-node-a[node-a] ..-> dl2-gammadiffuse-node-a .-> |dl2_to_irf| irf-gammadiffuse-node-a
    

To use, you may run:

.. code-block::

    lstmcpipe_generate_config PathConfigAllSkyFullSplitDiffuse --dec_list dec_2276 --prod_id MY_NEW_PROD 


