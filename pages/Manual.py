import streamlit as st

st.markdown("# 사용 메뉴얼 0908 기준 ")

html_sidebar="""
    <head>
        <h2 style="color:white;">목차</h2>
    </head>
    <body>
        <ul>
            <li class='num1'; style="list-style-type:decimal; color: white; margin-bottom:10px">초기화면</li>
            <li class='num2'; style="list-style-type:decimal; color: white; margin-bottom:10px">타입 고르기</li>
            <li class='num3'; style="list-style-type:decimal; color: white; margin-bottom:10px">입력하기(Base)</li>
            <li class='num4'; style="list-style-type:decimal; color: white; margin-bottom:10px">입력하기(CSV)</li>
            <li class='num5'; style="list-style-type:decimal; color: white; margin-bottom:10px">입력하기(Model)</li>
        </ul>
    </body>
"""

html_main = """
        <section id="scroll-num1">
            <div class='num1_container'>
                <h2 style="color:white; margin-top:50px;"> 1. 예측하기 [첫화면]</h2>
                <p class='num1_content'; style='color:white;'> - 동일 건축 프로젝트 홈페이지의 초기 접속 화면입니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypCnr-BOtMZ9hT-iWELZY1Pk4sMXw5xd6_Os52DBFDUnxsp9aIfQHFgqwPiPowNLV9JXwz6CmpT7ZwPmz4mbLYZMEghlHA9XMyZYqEE4PMLp3-xJj2Edh5sOkGHL90J5Gm7hMNhT6cR19I7ZdibHmTcdNT6Q2ruCh1xtwmfDuJCPL3NzRsv_AKkcaOfvr4faSvI1onBmd6p6AH0HNl7GqmSCGoWou6vHc45ZPD-fn5GoxALErrjf-SgLwQAsOLh2j6dVYy89GZRIvFp-EVj-l0wtmxOW1JMl7prgU67-Mf66ZAyGKytes9igVU23Y9U6YlAzsCatPiglugUoYki3_kblM7jEs5GCEhqLcPW5YfLcSuUnZypI80fYmUbKqlP1TuXBQ00p8c-Zu7aqGdg9sPPznriEQtQY77i1t6GIcXqdqqOHnJYQ0Ub91ICjD5rpQxBXSjToqwqfVqeb3A5fH9lcdRxGywxPk6fn6YNDWKhRolZscgM1_utxxm9k0gUAtkVo4K3iWnjWDbMBsCRMrTE1WnlanrwKMVy6j2aLyNftTwWEklcwnxEX6qWzOOHNxKcNpe2TAnu09ptmfaKgUgaoWrC5vKj3ea9ehGVanYfm0gDY_3scuh7Is4MSw28TpK8NqeN9Habgcmbidv_Ijd_flnMOaoDVULO525D8oY5v4kr4NPNi7k6VJUqrLiuOISCQyPgHTgnkZDJTurqFpMrC1fevKDzXMjG1MUcvfWDm1KWfcJdbGswk9GEx1H_-_2W0pJ4KoUH1O8gRW1KPnWGmiDEI6YSMWjGRHHGos_RsJUmfViK5hOtirberQlKazJhQcr0tirOlOFh8OpmfKDoMGDlFyb-njde5v9XaCKl6_4PDZ1KkuZInz1PTsYZWlHZmTaezdJhVJMSdH4y_cfU7BqlsdqdALfsE3G_XtAwJCWa37OFwaCHFYX_4BmVONrEyHKZW7-1Cd_pjqjfXt_puv6Ig5SRJHmdNPN_OGhEaZ5BsuVi-D9n463-ot3CFEa1FE55dRRB_TZICUE9DHpLmQC6xMi9bTmotQ6ivpSeRxjdJPVpkSCcOXOmAtVFuU1IfBCtTDo7B5RD0W2T-Z0Gd0k74eih2EmhHMWJWB6foPBEr_8s2CsigKifD3gOTuyTxESATgGPlMkoLyE37VV4Kah83nZ8_sAvlUnHIwYLbHLMofdqk4vMo9lq1IogPxXwkKqSU3JUF3H91OC2z7sqgdvttKgYRGjha7KqeytAvCNz6hTn-6tflDuWA1hNhdi1w1NTWyQ=w1920-h1080"; style="width:90%;"/>
                <p class='num1_content'; style='color:white; margin-top:30px;'> - 메뉴얼 페이지와 예측 페이지 중 하나를 선택해주세요. 설명은 예측으로 하겠습니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypBjnYTMmfPh-UAf8_EDuRzqWJGbwp3WGVSgJgxBareVm3TBRurWyCEv8x1jkiIcOh_4NcDQZ-gUIhJEIGJQeNxP2ENYUqw4_tpkrK235e8vEujKzD0p-A8FMRXBZqraE1GdJksTF1DE6FFv566h7skjxsE9EGlRkcZ91AghS1srfKcmkpNVnVYnAIQJRvyVBqwgq3PTXM-WbKhK74o2HNVOJ2aNVF14KyEKMo8uoZnEc0Ye0aEZrs4ipBCOsKN2tGAqUswn0yuldiuyZxgsavugrVNaze8u4wn2wXrHsnlbSy8XRy1JNb5JlxFz9OkWwvclajdslq7H6FJQ2M12ocJRd4NoWMDxS_eruonq1D8yCdRwIFRMds58dVozWhwgePIMVy4srmjvu--I0Ygrj596GtZfCO7Lz5GwYjd4motJZ7QY0qJq1QOt8i568pcU0UfliAr3wzUsMzw0NRgC7d4b_kRPDS8YbrUAHkUUt_SBuNuvYmBwlRWy90L26MJVCiWp-PdhOlCy-IcLr4bAy1BGjbIBrteu-VDTgpqK4UQGFaVxXvE8ZUg1c6lHjOaTccjrVepfe4QIOK0ux7CJLV9bat6EHp8qxxQEMIzdDsvPxMpofsS0L3n8SoEIXskwsFs9LrEVj4mVMkkkheS6jv4EaDwXGbJqttjKm534sc6UnOhXzvmpo4XQHUyvYfCDuA3YEQaKO8EBaIlkif7v99WGufPg2D2Dgg24_46YLDQkc22liTQQrvFLmoph6wouo0NlGglhq6c0QLcZKfWapVN2JYvYYq-gxAlD_Rr0xFrIg_dvTSx3nXSYJpQx8a6J62vk79KwlYQ0ypT-fZs_rlYsN6iW-iZQL6a0GIQFdkXf9XyC1yhx8_AgwOcEkICrpJjp6Un1bvH9_3HaKclZY7oBlByHWcUENwhuHDtB_jDKmrjnkzNhyIi21jEXAz9vxatOOVzRLw3n2Zw444en6Lb8XEu79zguO4zbhftQGV6yUFlX75RkwV_AJT2n4Q1ivHkvC1VNCPnIqocopMSXVc-uuzIwk-ImzzwfNHXsr-ILqzDK7JERW-Nlmyk7HtuZq1qVdrOqTlUrJyDN0mLwKu03LVLQWf1XykLvFiWu0CnO37NnKFyJ_O3X-uJQZ-hglIKMqAgcV2W8eW1ZpluTEtbmfkMJGUFHKp3ynzly8lnUra0vxFGENli3J9M9zASg5TxZ64DxXvQc_YtalmU_r6bZN-VUTQCZIp4qaVSogltrRdWnKEMX7fzIJYhgK9Xe6CujAPMBhg=w1920-h969"; style="width:90%;"/>
            </div>
        </section>

        <section id="scroll-num2">
            <div id='num2_container'>
                <h2 style="color:white; margin-top:50px;">2. 타입 고르기</h2>
                <p class='num1_content'; style='color:white; margin-top:30px;'> - 예측 종류에는 세가지가 있습니다.</p>
                <p style='color:white; margin-top:20px;'> - Base는 모든 데이터로 학습한 모델 ( 속성 선별 x ), CSV는 엑셀파일( .csv )로 새로 학습 , Model은 기존에 학습된 모델 중 선택하는 방식입니다. </p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypC-S1Gi2YIkJ2mn4uurYpgrEU8PECvuhIWs57BGZaFY7hpORvFe3dXUZZKzhRyrgoNICcp-wY6Xkp0-q1oCX6SoYu3M2YIYMnQhRl5UyQTXYEdBhBl1uYoOD7G1kIFtvG25ST4fmvdyQ40vYTh0fPkCedYI_z9GN2MBmLjNoRYD1QS_LpCr2QXZ6mBNKm7XWucCsGQLrOGDwpTvw4KZMuJE4L_qKaxWeEARXHsx7mJbmg4OgyP3H--XevHfh8lPkZK4kIO3QLkb2iLT212gYv9w2gDM_ebjmYIWK2lAqPMdJ90flArlzujW3S0F_yva4xQevT9LoAbFipsZEGyo9pidXf0lRdaamZpD6ZD2XpVVpk_GuzS_USfKV5vCqAauUXeyq1nct_xvTjWT6Y_m8INcsjDiuFn3qlClHMXsuChda7J4Wc1vnFYxIl5-3roXd64gQLQsrAMl_ccuwt64rUfgHwy7WeTa0vLa6URW-EJyfLNCTHh4izJ7LAcZeMyUpgD92eSaLi-pxJQQjomQumTeUQb1Yeq1LhgxKHEzPeZheVdH9M0At5v5P7AH3qRP8JNqY-hPR1ub1X7ujnVgllAPvvpokeXqoKfbgfSmgWwPVIo1o09fDUEXtiknGzmscI-C9hA63H2ubqRkM9DSmPw30UWkmnGzBYPsWtGSl4H5FRP1uvtoDpxW4vlL2phH5yrV_lrNhEvLjZ5KvToJ7uF_wNyHV42QsKPAmtwvtPlAHgcGRlMnov0yfZZKecMUYLlsWaD5zJ7wUtWksUFfkMyQDRvt0GHkEsB31Uab9gOexH30A4bHSEef8AITThjwSO_mAaDn1-7HIZ6aHC_rayv2yr9BlZX3SYRE3c7WqPOZMQpJfYsMfD3a1cDXj20u3qt4uDLFRJMvxmSjcBeFokYnrhr4ZRAQj6qVJ5S59Zlc1o4jSnBuE2I71QbqwHPqnjmJEhNR_2xHr25ZcIR402cuCmYh4hAS5Z8PUglpxAZixXhb1kiMEE30ZR1P0JqCPsurzlhjvYwraI5xj_nuhtOD57PVFcotz5vbtWjd__HzeASGFU66fshnP_B_uG3HCzxrIIMKZfv1efSO9w2lYxt-dcc9nbjiY2VBmLvN37XFSyeFZTaaJhs1r837P9NbJ4nvlQoGo7Nc3ES-5Rpbr47ZPJ6pIxJvmIjWudKFV8CyWfMWtMmFYXzrVuw-y9lS73zkKAY7jfT8gRXewyMEkOWC59aIMFiGUgfP9TyJst6Z6E2KdIkENAfc-i8OOAPyyKhlCwv5Hg=w1026-h969"; style="width:90%;"/>

            </div>
        </section>

        <section id="scroll-num3">
            <div id='num3_container'>
                <h2 style="color:white;margin-top:50px;">3. 입력하기(Base)</h2>
                <p class='num3_content'; style='color:white;'>Base 타입의 초기 입력창 모습입니다.</p>
                <p class='num3_content'; style='color:white;margin-bottom:10px;'>공고날짜와 낙찰날짜의 경우 클릭하면, 달력이 나오게 됩니다. 해당 달력에서 원하는 날짜를 선택해줍니다.</p>
                <p class='num3_content'; style='color:white;margin-top:20px; margin-bottom:40px;'>다음은 낙찰하한율입니다. 낙찰 하한율도 마찬가지로 클릭하여 원하는 수치를 선택하거나, 키보드로 입력해줍니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypAg45CD0tb7HtG4fiyUZziLVrbXFN6b_QUXfIDyv9guYGTYr9zFOLb6ENun6EV5Fq25euB60rJqn9ouzmg6FQzZH9nhMyg2vLk9RJ13t1ySonjgL6HMasZL7hZRTvHZJkh5q64eM4lWre152ZP9ehG2kRmYBuaDe_THV5FcYmtNAT0RA4vG1KQyBT_TJnUcLzkdeDshC21xMVMhEoaloi_TPfaH2T2pGBgXwcJX1peLVR1bSbYAIHgtu2ngtSQrgJ0C00m3L5PuUqiGpN95sRaXFouBsAvoeFRjp1yrbGcvz65b3LqbXRMKGVs-oZu4HtCmGQ82NJhCdXTF0MjrushjioZbKfnvJ-WhORKMJujIuNW9_-8YyTTTqw_YGfxNmXnoNCUISKyoQUXp6Hr9NVmfZOS5JeQrFclPtAccvQhjue9S4aMIAcI9FWWPsMG2bfOnQy8xy7AlzoseldzRs65-biIsrXem_jLn1In8ev_S3dBlnY0SpQpBhvYSZQ2_lx2wcOPGgJQOaFqvUVEjAaoHCPzL49emvL75N-kNXVja2KKisrefhnAhkNr8_6iGC-6C0VhmTyuwFJzRFfE-rd9zzRfcIzEsyGTt_ZYQfphDdkWy1pc-2O4cuBXdqiZdgusk3LdH0Fv5ZXTiqk9WpDC9Bjeqcafn79jQiQQdUGaRbFGg_8MyAt4Uh4QQyOcmSpyts4nPX9Qcj6mEI0K0ySAiUWgh2lsnJH9gWnMh16nlvJ09jum0hyTou8PYcLoOd8V3iTXOGNe93kHzJKWdebhhmq114-78xcMWikF02uho-308-YQkmUHJFzP--ZfYwom_rM4DPqzvKAanQPOrOuLFgiKs2wb4cvYq41ktSFmPg_6_AnlzKGcPNApwd55PWMaJWN8_b46R5gdu1ovy0Cmw7KRqf3DakvM9owJfvlCeUSslNL5KTu45lU0n07dEQhDCmTssGw1cVchvL61kCI-l0e_rnvwZ4jmcCX6mxLWAGPET0DItN59a_d6HrS0uS0N9I6y2k8Kkarr7FMaKEcqEZ5A-mQ_JGWqVCkN_CMR0iH8m5bScvMibYeCUhRTeDsjBsZedY8G0wRxP9CQvfxTlfYLrmuYp9lXZVgzk8agRTGi5x6NBtE5BixZflpbSAl1wpbUmIE1sZOb2SmtuN-MAYKqN8g5tOJPubKpmJp7Nk-Kc0rPdRmaZ7xGpAGghifh7HPNMhYeyHh4uLTIeDmRcMxBOtPgRLsYoq7oNKwwFEPnAIOBB1QHRuQclJxNYCZ3QFwOMhg=w1026-h969"; style="width:60%; margin-left:20%;"/>
                <p class='num3_content'; style='color:white;margin-top:40px;'>다음은 발주청과 시도입니다. 두 항목을 클릭하면, 선택 가능한 발주청과 시도의 목록이 나옵니다. 해당 목록에서 각각 하나씩 선택해줍니다.</p>
                <p class='num3_content'; style='color:white;margin-bottom:40px;'>그 후 마지막으로, 대지면적,연면적,기초금액,세대수 항목에 원하는 수치만큼 작성한 후 좌측 사이트바의 하단에 있는 Show Predict 버튼을 클릭합니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypBVA6xnOYLW0nKCfwx9FqjoyG64q-64AdgfZ56_EN8Ggyu0C15TgOWMF0voyzJL8oS5bx3ZiDq6G6Ka9B5grFk6JfPlwgsKHPXlqkIBtg0fU5kljk3dceArhHf9v9MDclMOEiaiFcaC2iy8PcT__b0fKT2bN8ysn_oabARcn5Xzh6hZSNEtOtwM9M9fxHNhX1CkiUd9SwXx-OmP7FseuF9qgCly0-jRkkwW1EyWdMJczcxcOt244rjGyHgTE3vDipQATGlubjsN4H4lsQWSWJ1om-xD7mOlAQA4YM5z6c4_Azs3_i4MiFGUucuxT_BuoPqUO091HJtpDiRlcvSnGqrIAIt_goaHwIPmLm_c1BnNZoRvmuU_1Kv6oahVfhy7SP97oonCXnB8ouX4RIsOKjUueXEKl9GY-Qyte4AdUy5Tj0GZ7qWqzEXbLOPPaUZ8cDXojXo1Z3ZNs5y-zbare5l_OSZrKvvRayxA79fPAJ1EQWiFC6V9lOn9eRGmcxS0GfAfZ2RG4PgcFR3KbwU2IyhNo7ChOWnIxBl163ey_lJ0OrXxXjmhwg48USj-0vAXzd2FRmFje43ZYUgh2AHiQUzt5n1SZKAyz9JHyp3jRATSulh7-KrEAEXmvJqkwKix7aDjlXlpBTLXPRxEoCVVmEndPvButJkFzO9rO9S2gYiFa9lt4z7SIatJHW-W0OSgtU_IHng2Dh0Vl3v4knMc01O6Mwq9Kq0pifnuEKrNSV6wvdfmSQJxLcpzSisEMRbGKDkLQqmK_bWMUSb9N-izxK-v7tIUuSMYZVe6hvOFm7YBQzIJOIsewWs_rL8SZDPn4TSLg-8TMsYg28FFDc04buQry7nOb-CG64V6kcJaSE-d1f3vbdmH3IdwLYMXLPaLRgh3l9yCnaK0OF1N8U-87tEnHHy8SuvbsRVUAPxopR5pAU2ZDlOJfnNxe16uGZ5kWoCO12btjuEavOOBdvd5DQ258QHrfKRvV-eNZcGgGyiCmaV28Crca98o-TCXy6d6GD5DvLaEOK0ySrWKJLs1yxXldxUaksPR2Rw1tULVK4snWqe_dzwmM3cBOPE-nUmvQz5T0Hyg0yl1RhMC2UgOxOxeVS58CJwULspCqiaNXRylhpuDZ03mdvSujSrm6DRcGYWyXB91KhLM4zUtDgT7lE8wUt7RLKGoe1d_OeKozFK7FEn2Kz4i9it9nHugWjmSMo2PeCTHQv3SYn139fHNIvoDUI6eKJ34giRSnRep2bhYADz9gXCmUmWGeHQt9_yFcB-ZXDl2FQ=w1026-h969"; style="width:80%; margin-left:10%;"/>
                <h3 style="color:white;margin-top:50px;">🏙 Base 결과 확인하기</h3> 
                <p class='num3_content'; style='color:white;'>Show Predict 버튼을 누른후 확인할수있는 첫 화면입니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypAMGCPh3HfO_fJ_ptmOznGjGc2LuK_RGGYVnBC8XUTUay18jeSdXHsUQLl44RUaKUFmlOvEqHCAPBgTOYy3beTSfhP0-JjSs6X6er8ZCt323pWNSuCm2brn1KxOBMeGIWZ9yEdcMGw6BRepdYUb-QMhLYqnH1kyq0tQVCGI4lUy7lkO4APTnOIAnBhN2Y_uk7eqm1UIPG2Y89fnqkwh6MQnvIgWjKFrqpxzonC-sbf9TxVFLKZ3w7XLt4y0WdEPJnDf_w8CfQqwHTOcY3ZWabQRLU1oOsCqSXkttgsCmZxkavN5e74a4gkZqq-oBHceBZxd5EENWhnSjVJhpxVh-b_UhydD9eDx0CdVOoZPW4otXIV7X3Wsnf9n8GqDD9iToVEZTjL00uFbNSJtKAMHfI4GZWT5yKnp98SZKtolossUsVD1WEnNDdMqU0xCNCYlPGQxmqMOjxzP23lwwqcDA3xaHFENlTGbhZmGt9xNJJmquBJi5PA-q13DY-p_RLHXpFuJIzAt_DaWpRLejtAoaR__dcKUIGaYgqBGws6VfYDegCBn1GVF51omDA5lLAoTdH89P8DdPrh05GbOOk6DcvpACgb4IzAUYaGEC14upp9XoCU8hGn5q-pLw3HQH9CILCXHJWq_LZPSR-f9tcFdvW0h0KOGMXTfALQGRgLu7Vi67IHFaWzgqhBGhOkrmm7Lq9MXvmviXVCYaLl4InMHm6iOjFVSFdKzPYQzK2OB2lZTEaDk9CruZFDpRIB09i2GX7JPWQoyjSPcK8XVfhQUfhPNK6O2qk4QJHVQ2Cwt67JK_bTEjPPrFq5WQ2oaRibCkumUbVHmohB3fwYw-UD9aYxeZ6o3D9l2fqfA-sYqLbdkYfzIfIO87SQd5g3JTpMSbvdPmGChMSDYwIl9MWXQOQdQsTOQquJGe6ApIhknq1tEmOOMm9mYBUjBn4i1S7iS4m2S8Z-ns2OOmLi2YLajUF7XE_nVymRYi5pAglOO0U-BNioFKZrGWLhnivovGOR21nlcK2kA4ZAPUWetcoNekK_zsqXZChERWpuwFBdfnBWQdo4QFn9V-XvhXUdp8c0n-1ocOZYNsuuXIQi3Wb4_oPnPsR23jaCEmaW2jmB-ByLXkTKdz9nXAKZXsZTQwnS39UK2YHIvwim_JlCI7JIyjF14oH70fkzL8UoD5mc_BelvM1XIK5awChfoMviQCsD_DYFtXllxW7pgl54k4GbeDezZ2W5-SGQN_5-EdsCV9Rk47IeouHUbqoNEDQmVzZ46XN5DDLWVQw=w1026-h969"; style="width:80%; margin-left:10%;"/>
                <p class='num3_content'; style='color:white;'>결과 확인 창에는 타기업 분석과 유사공고 분석 항목이 있습니다. 먼저 타기업 분석입니다.</p>
                <p class='num3_content'; style='color:white; margin-bottom:40px;'>타기업 분석 항목을 클릭하게 되면, 분석 가능한 기업의 리스트가 있습니다. 그 중 하나를 선택 후 타기업 분석 버튼을 누르게 되면 결과에 해당하는 그래프가 화면에 띄워집니다. </p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypA3fyA_bTislncGwoFdbKmkW2xyj1i3FeRv3_YJ0KLdDvZTFoHK8BODX28Og0LMNhqIANOW8sQFRbJTAcuR3SXfyYuWUOOshfst4-9-nI1rVRDVvsMKSFOccz8-LVOlsLnXLQPKXR1S5MMXC4Y3ghT3ywWBPbeBwLvV3qFyVy4OaNhmbts_ZBVu-wJC8aQ6Ipk7KxxBa-D22nlbVxidDuJNngb6GTCRI0LBoA5umMpww_z1N8Zxn88PVJtzfusYqU6DS9MXp7Pg4JXuqUP-ESPBi3wWeVHvioPb0kDVzWFW1zQZXkaOOWN54GGVuba_kUQM_b5S_HF-7FdrTH7kkaRyoz-BD4tFF7No40Vv9IKLGjltZSrxw49E-oLBLyaQs5MFtSb_ZFOCx_BJAUCbn7gi09TJq4JUWjgsMEcBUJGrJzmHn4Xqm3pVt1u4kYyjPL72txnQay3lEcpknfpI9s2AjdXvJNwZRjTUqHFIDy-QVUTI4sCJaHfxV74Eu2fwFCgOLhFvuDVaKTKa9r-JudI0Bdw8q21EJAwQc81aqCFNl8NaEW0yvFC2-sgNihDiNAi1uTo6Sl8xNMqMqb6zaCsmea88_znNnaQYmxlDeoYGBgucbSJSKR9xELPlkQtf3f_ZlBDsV4SUt7cluwOjUhsioSaRGxTf1Jug2jR4EWIkYq1q8zlaj1kaPXIDgZyOebmYvpua1Srg8hfOOxW-dXCW6kQyMVFNhUf_J2A8NqQDNIJvcC8C2oN4XecUKMcNiv1d_w8c5UHUZbaA0RjbxmMQpeSbnvlaL8K4qUDLA4ENBQBfwLewT1lTBPj1NfvftpjHGabeB1bNRdpf3pkHFCqvZnIfs5VSuEpqJXf8EILKTpnkP_AybzfW5k03b-a9naYSr-BTHTs-Ce3k-q3V4FJFqUyvU2XHPQ8vCfI18Zikk0wPTGZXqWWdEuBaqqEoJO2yLUZL3RGI44ic4l5kF5-K-VqeSMnRTn5AH-W9NlTvmQG5Fl_ZNQEpgMWjAOB4OvCQhxMHNqat5f0avylgguvr4eBnkAQM1O6NgRkYsgVBFo5w_jffbTq4152J3lzfrHRhm4SHqL3ufqklhYNfdwKHmTINl0QJsHa9NcQizi_ZLFTH8XOmnBthdQ5PJgwuXZByjaRL6bFlT1OM2yTo4b_WNopt7-B1vx9kCd8T8kxKe0UfpySmkPHJ3Cf2jGOrDbKyxL8__UuFNF4jaFDV0gj2ezNjgQfM6kCyhkqhrm0w38dxEEGRN2RAa7Oy0_Poa9I6dOL_7w=w1026-h969"; style="width:80%; margin-left:10%;"/>
                <p class='num3_content'; style='color:white; margin-top:30px;'>마지막으로, 유사공고 분석입니다.</p>
                <p class='num3_content'; style='color:white; margin-bottom:40px;'>유사공고 확인하기 버튼을 누르면, 해당 예측값과 비슷한 공고를 확인할 수 있습니다.</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypABry9sdPLnfFXdJEKOEiF6CO-zCRgvbLRby8glKR5qbIcImDVIf1MrQkB1_7fMfLZVpV2s5OEEOJPRQyFueyQzVs8K3MY-Sq6OVjHryBiJLPMddROPXLRS2oIFk5U7zlTH8YzBvQMxQI36VFBrG7uFw2ov9hn_IgyjMpYsg8WO6Dbg8na7UhmY97DQH9uXzXFXi2ggCkeeGK4P0p_u5HVfru6FaRQEg1JlWlBJeuHH2QYwHzf1-p4FQNoxSinGDVHG2t7X4tfoejc3XRBP8We4ljSWUIQzozm-JWbO1M3V90Fm2duqRFLn24Psee4Z3P8tcMxO_j6M3kHqmQl76RpgHpONX5KhZVj2zc4Q2ekSR-i4oR4Zwo1aqNYMV2gklaPF1gZl1EXp6pZjTlOv_4-LjDnQVn7aC_zYTtf08zUM4XE8feMsoi5gh1Qsrr6kfU4N2zkCiADWJNjhP09WNsEoSjiqzjVLJd6a8bnbm1OTlPDMniBmu8zF20aq2UAN1AlGattIgqlKUQbo0LatvXfVami7V3pmFPATCbStXqsOJYxV5bonMBzUXbEkBjKpK2JRZJ_vSvUijnuPnScZEDAX2c8-HYOWn8X5YBi1glfmO5kV9Qke9OT-cAyE2r6iCJLZgpuiaIgmkHShGcQKkmetA8K_h12qKh2tAwpY4E_2HQmt_A5JPGyCfgoiAJ6rH2lxo-7iJjIuS070llUyccfc55sO2mJ5e44Z75bSWy2Ila_7-l5-vevUlqKLhWnK4wRZT0Tg9M530sJgHRQXKph_ehquVIX-WkDBJo5OwB0ng8kLOkrd9l8j9qaufHBme-H5zX0XloLMS7mO3yW-ceb4cfqbiIpAnDhsdPZN_DkzSj-JVPBtzVuGq62wUjm5kIKgMhY22mzDD3sKjZ53I_onKyP8t4-vKlG7oqQ0GJj8ylHrRbwZ9uCwr8bHKAvUYfJ0gboF5hgkeeNS0qGhkBaEd-bUCG3Ry5ULSPuE6jfAYd9h0mWO0r3vXm0sHFhoELFWJtP4pYzNu_DTXjMrsBxFyumNTASWrh4_XNZcGThe0aeF9gXioniq0tyVx9lM_GmmS_QXRXZxrTpdQFLpmVU1uNhXkoN7aD_j4beSQouWZHUkUe75RkxoMgUkXflZnP5RU29WTyP_GfgdayNZJrc3oVEP9VDmN0q9mqln78ek4leaN_y12t2s-Pn193c7-2FHFfx05O3_hSJep-GN2Z48wVAeUZyPhCUbW2QCdYssZajkh3xQY1-xG0HUStC6xos3q0yGJQ=w1026-h969"; style="width:80%; margin-left:10%;"/>
            
            </div>
        </section>

        <section id="scroll-num4">
            <div id='num4_container'>
                <h2 style="color:white; margin-top:50px;">4. 입력하기(CSV)</h2>
                <p class='num4_content'; style='color:white;'>예측 타입에서 CSV를 선택했을 때의 모습입니다.</p>
                <p class='num4_content'; style='color:white;'>먼저 CSV 파일을 업로드 해줍니다. Browse files 버튼을 누르면 파일을 선택할 수 있는 창이 뜨게됩니다. CSV파일을 선택해주세요.</p>
                <p class='num4_content'; style='color:lime; margin-bottom:40px;'> ✔ CSV를 선택하는 1번 항목을 제외하고는, Base와 동일합니다!!</p>
                <img src = "https://lh3.googleusercontent.com/fife/AAbDypCy2gubG1yoPS28sdnpAn90SUslDNcOOzfQs8cgUI6yt6uUAmlUaFQx2bbqu0DNxmwPkTFcCZeqVpwIg0Fo7Zie8PvSReAvI8YKUHYmrwbdzKtzjZB9xLQZcSy3pcVsnYppFgQnHmxNwz6WyUC0VCkFYfw68Xxm-nHFdPNydfRSDtIjehA9yD5nvHn4e9Ii5AujyxI6hLUCK-XOpzemgatTOlPuqEUh9AZ7oWUBfMi93Vjg7Uf_cTGW2UrV2_TqnIQwOlBCCltMlsP3Cm-NuHe7cDk3ob79i0snMsC1TuBiMsGpMzhgxtU3W6MaNXuDWYyp4EjzduBIQxyOrmJEsm30UHRebtJi3ml41_TxG_X2zUTfeO5Pb86U4G0t3ZGAEZG9ZF4kpHnV538mCm5blegB14IDtF9pCHXw3lHENQg8eCDOngIa6ndj4VBZnuOn-u7NDn_dcnP2KixOE7pY3hnS0dzFfkKc-mWQjwU4iUhR3FsB_knuRxI5IsCj5fIpRT95AwO2Z807FrRAoGcvmhtD6jnbQuKn6XpOW0uLiexBQeuxHdjYdIGNu2dxAgtA4lvtW1tdy9GPkDELAZBMBGshCXLNT4OXLXGc4HPgvz_UVOwup8_2ti2woPTy2ozqa51-3dAqRjsjP6JPceFxTDU2VpYsXWiZ1vztuz-dfI0OIe4-iYtBqJpZk07nL8Gzc3Erdh3IIEp4tpEvYcAL51GYHKxpGx9byxKP2qEQFFMUgwGJ0J9MDIFAAF7rGsC9oRsY4h6MK2f2zIxx52kHZF8euFJZpOtBDDBjsbZcsuJ3kEFJ9yQBB8op5Afn0njzav0j6BFaBzFJaTcgoAvIm2Mlev0h3iGn4fc0TYaakZ2a_4qAYsG_I_5ku2bC-lXHu9Rruumb2SaZ-7qazhLFAqM-QhjPTTuvepK4VCSWOfJVZlnu5tIWuYStROtp4836A3XZG5Y6I6NS3Pa6LY26gy75rKef_lYq9cHoStxPjLvLbcUWvHl0jrlkttE8wX5HoY2CxSN3qAP6lTXWOIEnrhpIsxX6CjiCA35Qmd9U2ml2LL1v0AhtjI81e28ZJOiZMeDUF2q2iCOmGwUMNZIBjAVz1wgOGHSZIe06ybVW-ukaDbpyE_d5wvoUimaz0uVz25wn_s5s-_8VT4MjFnhwXcVjhPDrpms5Fz5hRZEh7mApKdlasn56czK0H4JMGayCuy9c9wqxpLUS0AEpaQTL3b_zE5DvDDvfeTnwx_ngNe3BTIL3phmL2sLDxNbAF2bux9dtgQg6Sg=w1026-h912"; style="width:80%; margin-left:10%;"/>
            </div>
        </section>
        
        <section id="scroll-num5">
            <div id='num5_container'>
                <h2 style="color:white; margin-top:50px;">5. 입력하기(Model) -> 미구현 </h2>
                <p class='num5_content'; style='color:white;'>아직 미구현 상태입니다.</p>
            </div>
        </section>
"""
with st.sidebar.header('Manual'):
    st.components.v1.html(html_sidebar,height=500)


st.components.v1.html(html_main,height=7500)
