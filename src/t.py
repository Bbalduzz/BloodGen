import requests, re

cookies = {
    '_GRECAPTCHA': '09AJ_RfJmCgh2F3iXVIyvjHBFuLxZ67i_piJeajHc9YqusTeQoFkR04fQhP4XNvnNDIzP2KWiO1KjvrEOMCg4I94k',
    'NID': '511=MuLWXfzK8NLt3P6SWvc77oS0O73Rt2HDYTa1JnNAO-DeEv9KUqXUPlT7LufIN-UI4QPcvJILSk_1I0zyP_yORkHOJx6bbQPUB2LVnVdL15FqCo6BcC3n8ZcHGdixBIJTYjayK4d0tcI3X4ROqp0kTbU8IvrJo5xzbFB3DjFj0vEdFIYuVhw',
}

headers = {
    'authority': 'www.google.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-protobuffer',
    # 'cookie': '_GRECAPTCHA=09AJ_RfJmCgh2F3iXVIyvjHBFuLxZ67i_piJeajHc9YqusTeQoFkR04fQhP4XNvnNDIzP2KWiO1KjvrEOMCg4I94k; NID=511=MuLWXfzK8NLt3P6SWvc77oS0O73Rt2HDYTa1JnNAO-DeEv9KUqXUPlT7LufIN-UI4QPcvJILSk_1I0zyP_yORkHOJx6bbQPUB2LVnVdL15FqCo6BcC3n8ZcHGdixBIJTYjayK4d0tcI3X4ROqp0kTbU8IvrJo5xzbFB3DjFj0vEdFIYuVhw',
    'origin': 'https://www.google.com',
    'referer': 'https://www.google.com/recaptcha/api2/bframe?hl=en-US&v=iRvKkcsnpNcOYYwhqaQxPITz&k=6LesejsaAAAAAL2ZEuqp_PSYx24M0XYyFEV9M1Wt',
    'sec-ch-ua': '"Chromium";v="109", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-client-data': 'CILlygE=',
}

params = {
    'k': '6LesejsaAAAAAL2ZEuqp_PSYx24M0XYyFEV9M1Wt',
}

data = '\n\x18iRvKkcsnpNcOYYwhqaQxPITz\x12ä 03AAYGu2TOgKGs0VHy7srQpi1MNzlPYQ1Z-JQLg4ZQ3E3qjRE4kTVAESJM-SjrGxr2ae-EUb0UQrFVxnkBUFvq87GvK4sKd9JWQ1Ysd8fbBqyIkewzIpzUiCDN-TVxyFOskEPYEhkmfGn31Hn0VBRupkGZOsk6MYZZtnhrTQL-ogHkJFDCclKscJb68eQ1f3RO0NtR2UPI8Vh9F5AvcLrazyMbGAX42QjSXxnXo1UdXiPAdvlDsYB2RyyTLGCXunPnfgiSuZZneWT50e4GxCylg9lsTU5Hpalp4abnRXdcPphpNdRdd1iHOixOSQX1KPQFLLoajJUOwa7fxw8VLk66zP4DVVuR-sT4oXDB-3ORzmgRDIxo--V37yAZgHeNkwCdPFdFd-yvjh8tYe_zmqq2b5LT-NKzeigXSZjSgcoydBvKnFK6VadyWcMod-xY5xgMUsX4rvV5EM18wE1gDC4X_4CbrCx8NL3VGjBLuqdFOU3noXVG1JYyUy_UxMlix_5KQJ8-7710ZSAomtoFqvrdrPU3K3u_CDls4A8hU-j2kySEmaDi0XjxcESyCssFQOU9gNHpWm9TxU9728S27idlunZbKzYfIGdGhvrV1rK8XZQ7n25YYfCnE-cMthJYcCWRBB7HcG19lhs7EfzniZRT_luSU-7Lcg9Zs1V7kBhP7E6A4MLgfusOy6bNCw8ajJC4XEKj8gtM9Or55Z5pVNQEVFNnq8o58jjgQdoQc0fDzvmLWdZDKXJlJ6BeJMl6008yIeMDfMCFETBLnVxHAOYBYNDMCbMGFiZA4ypvhzVG-kuSJOPFzINlahoic6m7Dh5IkBCAKeeNP-IyqhNfMYKKBjvi_QGiWCjwN4xNVIl8w1QNQu3pIe7e4Lt2qkeqn2JOOZB0kCpQ4Rz6oxuEt9FGv_dt3yNMY5S2DibIhK0dxta_SXE0yHBQntgzPMpFfXPJnSnm4BqWLnfZEqr51WpIXQUF9XI6zBD4IMYoImhsewhiock0y7MhjYkvmXiyWoHLGxZ-QTxJu4WPpB4phtpOTAJlifsPgt3gZfb49_twAjR_qgcbJyj7vwAVLHCy0yptj37l-dScnk9uCuROKoPpY0XZkjG6orlLfR24NfkvH9waFHOmE7VHJEIbXZNjmwV4tEQ21ZxGswMg2uZb2-V3HZrNyxGVRCLeezrZfFYccnSVaCkUM9NwqWHpMy-ZrVtDIu-dP4FZJ0f-vkl57cFlbO-Im9SHN1AYHraYkRL_dOdf2tS4RFcO7pDOGvD6I5byqpMqZc4upZfLb2K-yXhUlpoWPiIAnp9dnElrauIBO8fnqUY3GtQ3s59TavGjI-Ei91BBz3BgwzqFXV2J_kFMHWMSmFsSAfz9TrFpzHcwGSJJ_UIl5ms_UgWUZsLq9sWWVwKmgX7UARaUmgZqjeMgv4IOgWQErM83vRjs6BkRHKTau5yPqDhYwgLtW_eM1Llr_Oc-c5AK9YpWEiJJSY0K5DbABTzFaxH-djHSfZJ_Y60qUdKLfsh4_gErju0W9t76JQWViRVBn594rxf56uv7p7aH9zzSKUeneq-vwLiFHw_lPsObUDO9BpVjRG2z8ZmTRuXMJSKwxmOb3Iq1xQfl0dvwNYK2D93S2XiNtZFluDtYEP4ghE5cywbhbgT-AP8RwrW6x-B2CUAxIktxf_qc3KSu7ttkqCFJ9TmZeRe4VlooRGnREaYv-O5Re5KE8QyR_bPBXgwyCz5G3O-3ZRJWpsRiG4BiHLAHbnwnMdI_b9Bugm-1nY8A7uzRqlRg94G-q-bgGN-GXyfnwRUs5a0mw6MbWx97BKXWhXV7oKJgyfxIyv1oYKpFF0kdnYlPt8GZSREKNMB3Q-7-oH06tfSqJqGWlV68HWR2JR1ZRNCzGvVwu8MKldzJkZkOll2QMOeVENheOH1fDBK9GPpakvYd308JQUpm7py_T04vSPiZ49S24XfoNQCeUVuWHEkTg-IQTrGlbPIwMvKjsnVRGUqqUsY_w-Gijsrwy-3iWXnc7RZzRIyH7VEPuQsbs5SU6E5qdeOU5U0e8v-v_oTt1Ndd_fdWxsONR_SWynQgkgI3Zp7GP1HRTELkPxmgRMY8afFGblyLBP8wpc3haj6cUPyWDdLXzjVMxExNHFdgx-2PmD0bh25RjOH9ShYEcnbma_grQ5gReBPFC1XRduoeCApRY1gSx9JiW6Kvfcd-aCMuYXxfARH9ZPYI-QCfy2hSgeMIVPf_YC8TYfzu6bmD5OZI6L-_Qcd1gA9m8pNXVKxVpClEjtZ7t2RcUi_7pF-JxaFwj1tw0ABdWWR4-plNWMu8gsgYJK2b58FdXC6iBEoXgBixV38irMjCaVw85csL9WB5qjtAaMgKV8_yIHuXH25mC9k8sd4Iy7hXIkC6YjFlK5wceVuMj7OHj5-CLnPAWqsZ3OvKGd9s4oyUkRJ5ZwTn7847T8lgjBWpb1qw3BiOU96mq0KeUmhBf1UuwK7vs6-FTSja3dKGWiTCSfWfebUIxgSxrtSpR7h2o0mvFaXcIqwjrghl9pENJervk96M2BsVKcux1DI03lT690JC20IKxIQfkTtUyPQySQ2nW5y4Aczi8BO8RQ0370U6eLGLn249sL-T381Hi38T5BMnMp7bLiHLj68B_IFx3ZyZqNXhEACBTt2fhPYXeex2suPWVK9cBaMu33Z0hDB9TCqGbo08ZfU1S3qgcGAFKM2avLZ82wX__GawOz-_dHVfvKlecbNcgf5xexVwx6deWHNsfdpIdP2eJrvh4gKAgjThzR_261qpX6uuyK3yHEeCNeERFVm4NM3A6Xp_HiN0hUUlKvTOwxfTraQVRUaEZbvdMrKWufiJj7cFvCRp7zUr-a1swDE8IPrhDck9w3PP0ksrqxw-oWT_lTdMrBOUv_XKvAF0dzWtuGFcIcXzXHFcPLoows0_69q90cz1y1yjU9Ww1NAVwPpyOlWz0H9FwbUMN53yNlr2OIjzi5gogdBwNVSAK7S08ioWhNjGSKjvp-mwW3YnaVkqJzDx3zhp_8ZU4IPs0T9JzYt1A1EU0OA-AkVU7In7MFq0OYmbPb5GW76HEKBgA_AfxOXg4Z_hpXYLGXWexLWGJevwGnXwE9NnKZ50D8vwHwHhGh8wbpICc12xcEpHNG50LAfROtvxiGpE_lEWEvXjymniSQ4bR1xZGQFn0TVVB3FwMuqOiH3Izk3Q7-q0QS6ygxvde0S0k-3NuZt4zr5-kzVdp2qcn4GuiTE_MW3W1jAGDPjOfGh-QjHxyslEK4UEsHPXzUawUlYLUaeo9JBPmpcT8vx9UH6_o0nuAp-KjpmyokHvb7qLRyWddRZ_vDdn8JlFJMdDbdV-tECliQviUxPLoBL4j2bXftXL-18nQOArNh3bhiLuCOdrr9Q7TA_2VOelDllcCCo2_DmMYrU39-07uUkLa-X1dYtwGxaZ6rzkrUua2LrUwzTztavO9O1_CjoSqmnvwmlXnhMqQjeH-XsgLWWh0X8P43E_3B8NpmETPZm2siEiDOZDctmA4UJgp02cD2WB0tHiZIGLDPZUEt0abenMkVNjZcX6hmspJBaljgk9of1e-3tTWoUb6xnaWYeslYck2BSsxJcLMZy7gZvHkuwCaqoFl0RyJjLN46nYYNnatkre9uxLMNUvxHku_EfYSEj9S_qDPEsOsPdVKkRSUyXuXf9hIokkXwqqXarscJum7Sw-B1V8aasFvYib14q3i-s03ImvqbivOOvvjud-FXbEv2kXTKo7DeIsvX0Bl5CFVTxdkV86j_Iozy-bt5MoPTiIlBqnttY8xXo0iyszxfXNPGRrsSyPpVlW2pJxL5FBOWc8VbztIDj5PuKoracT-aY80Kn6mYLUZq2aZ5ceFTaWNI_y5Ne0bwzIZWxXHy92d-LFokRCxbcMHMGRnT3SF43of55X3iEeoQz6ITYsyBm5VoXlYoDligoZ1ZXYA2GpoxhRKqxCzSlFz4PLW3ThLwSM1gWodUyIGwcNkyqDZf6qI2f6XyWq35KMn6DOBxIV9G1EzvF_5qNiauZHCDQEY-HOX93MnjoiN1GIa2JH97GLNqd0Izf9m_clvw9fOGGZvjUKoySfBo2H6iKumP5e3ncKC4Wwg6UkkA9iNlD_T6mfjEUy29l0I-SeyvvrdvO5cb1bPWr9VorkMSS8YfNa58xzzw"\x8c\a!CQ-gDwoKAAQeBGTybQEHDwIXKnBvk9_0bxpGQ5IZ-dkl86Xu5hRjsLRJ-9gq49AZDC8puKHvS25aUSV_C9oRgZvXklVYRCvutc-wSHCzLgvKiZ-PavM4I38aYavRl3xgvpOx_CfQlvvJMXQjRzFPGG-94-_-ZCvqeTrZ8uqE8oXExWVqFmem85ZQQI6OFICaegZKzVW_pkewy4zYkQLazhHhWQO0b4lECMEl3CZFPeidK7AdPZR2L4Mu-zcif1yZlFECEcC27wHnqPNfUJqNNFFjSPTMy6QV9FcrE0pmSe13BvR4lqWZsdLiUqoGO3ysWJf3HIFtWA_ezGZrHGaduENNCLhQScAcF2EW3GaNDhIhba9ljT06w6iyZSA3fpemJ4jKWSq_UORld_cGoLa6_QD7ihhUWP74i5Y4bJiJraE5cVO6xkyGJWphog-pdSXzWbGXnHHcCmakEMCstwLbpg9Lo4WYaSYCoL70qcea3oZVc-_H7NM8f0rY8grxOJ7XIc6SaAQJZx-E-XVo95ixp1n06azQUQyyXrlTuojh4ZJXDoSBqFnaF2H4S8ihguw815hRFhCTDo6z1eU3I01D7Tcf_vl1sj6DzsdXPoNHU42AjnZHasao4mgQq4wIbvQ7G9lKT6obFVcfIZMqIQC55HB7T7TvmrJtmZJRHh-xCEugW6lnUohRsIAUw5M4uR3fo6mHdxUpZuZ6Ijn2doXasKsQjFPCWKQpKpwAfLExmTbGnMZp5YsUPbeA6OMUflHGHhYD4qTkeRDlzPoC6SvfNZ-pCsrbVaF8JU12vUDb29U920Se1xVMjWRCe_DHfzJZnET7CvbOa_MOCQ6DxiN__dEvQXiBcHTsZjnEVupdHarqOaGArK_20ERIG0LG2uJ6APu-BYXyRoE2\x01rr(6LesejsaAAAAAL2ZEuqp_PSYx24M0XYyFEV9M1Wt'.encode()

response = requests.post('https://www.google.com/recaptcha/api2/reload', params=params, cookies=cookies, headers=headers, data=data)
print(re.search('"rresp","(.*?)"', response.text))[1]