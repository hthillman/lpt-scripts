from utils.livepeer.serverless import orchestrator_performance_status

orchestrators_with_status =orchestrator_performance_status()

thoms_list = [
"0xd0aa1b9d0cd06cafa6af5c1af272be88c38aa831",
"0x86c5a8231712cc8aaa23409b5ad315f304c09531",
"0xe9e284277648fcdb09b8efc1832c73c09b5ecf59",
"0xe0a4a877cd0a07da7c08dffebc2546a4713147f2",
"0x9d2b4e5c4b1fd81d06b883b0aca661b771c39ea3",
"0x9c10672cee058fd658103d90872fe431bb6c0afa",
"0x942f0c28fb85ea0b50bfb76a3ecfa99861fa9b4b",
"0x731808ad8b1c3d13e8972db838ada5fc6ae3c2c8",
"0x4f4758f7167b18e1f5b3c1a7575e3eb584894dbc",
"0x4712e01e944802613de3a0a6d23274e7e0243015",
"0x43793ab4a56e5d4c263e6320d59072e01819b6c9",
"0x3e2b450c0c499d8301146367680e067cd009db93",
"0x16f7ad09174a9c1734bb446f7371a1498edae24b",
"0xda43d85b8d419a9c51bbf0089c9bd5169c23f2f9"
]


low_performing_orchestrators = []
overlapped_os = []
non_overlapped_os = []
for key, val in orchestrators_with_status.items():
    if val == "Low":
        low_performing_orchestrators.append(key)
        if key in thoms_list:
            overlapped_os.append(key)
    else:
        if key in thoms_list:
            non_overlapped_os.append(key)
        continue




print(low_performing_orchestrators)



