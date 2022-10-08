# ---------------------------------#
# 라이브러리 선언
import streamlit as st
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.ensemble import ExtraTreesRegressor
import datetime
import os
import glob
import math
import zipfile
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform, pdist
import xgboost
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import StackingRegressor

# ---------------------------------#
# 페이지 상단 표기
st.set_page_config(page_title='수주율예측프로젝트 By 데이터청년캠퍼스',layout='wide')
# ---------------------------------#



# ---------------------------------#
# 전역 변수 및 모델 미리 선언하는곳

# process_dong_model을 하기위한 전역변수
scaler_1 = StandardScaler()
enc_1 = OneHotEncoder(handle_unknown='error')
etr_1 = ExtraTreesRegressor(random_state = 2)
poly_1 = PolynomialFeatures(2)

# process_data_model을 하기위한 전역변수
enc_2 = OneHotEncoder(handle_unknown='error')
rf_2 = RandomForestRegressor(random_state=2,n_estimators=14, max_depth=100,
                                               min_samples_split=6, min_samples_leaf=1, n_jobs=-1,max_features='auto')#,bootstrap : True)

extra_2 = ExtraTreesRegressor(bootstrap = True, random_state=2)
xgb_2 = xgboost.XGBRegressor( max_depth = 3, min_child_weight = 1,random_state=2)
bay_2 = BayesianRidge()
stack_models = [
    ('Extra',extra_2),
    ('Xgb',xgb_2),
    ('Bay',bay_2),
]
stack_reg2 = StackingRegressor(stack_models,final_estimator=rf_2,n_jobs=-1)

# 전역 변수 및 모델 미리 선언하는곳 끝
# ---------------------------------#






# ---------------------------------#
# def 함수 선언하는 곳

def dong_model(train,test):
    global etr_1, enc_1, scaler_1, poly_1, path

    train = train.dropna()
    # 기본 변화 날짜변환, 형식변환
    train['입찰날짜'] = pd.to_datetime(train['입찰날짜'])
    train['발주청'] = train['발주청'].str.replace(' ', '')
    train['시도'] = train['시도'].str.replace(' ', '')
    train['입찰월'] = train['입찰날짜'].dt.month
    train['입찰일'] = train['입찰날짜'].dt.day
    train = train[['예가율', '입찰월', '입찰일', '연면적', '대지면적', '세대수', '기초금액', '낙찰하한율']]

    # 전처리_1 -> log화 및 std 화, 스케일_1 저장
    train[['연면적', '대지면적', '세대수', '기초금액']] = np.log1p(train[['연면적', '대지면적', '세대수', '기초금액']])
    scaler_1.fit(train[['연면적', '대지면적', '세대수', '기초금액']])
    data_scaled = scaler_1.transform(train[['연면적', '대지면적', '세대수', '기초금액']])
    scaled_df = pd.DataFrame(data_scaled, columns=['std_연면적', 'std_대지면적', 'std_세대수', 'std_기초금액'])
    train = pd.concat([train.drop(columns=['연면적', '대지면적', '세대수', '기초금액']), scaled_df], axis=1)

    scaler_1_filename = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_scaler_1.save"
    joblib.dump(scaler_1, path + '/' + scaler_1_filename)

    # 전처리_2 -> 다항회귀 진행
    train = train.dropna()
    poly_arr = ['std_연면적', 'std_대지면적', 'std_세대수', 'std_기초금액','낙찰하한율']
    print(train[poly_arr])
    poly_1.fit(train[poly_arr])
    poly_df = pd.DataFrame(data=poly_1.transform(train[poly_arr]), columns=poly_1.get_feature_names(poly_arr))
    train = pd.concat([train.drop(columns=poly_arr), poly_df], axis=1)
    poly_1_filename = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_poly_1.joblib"
    joblib.dump(poly_1, path + '/' + poly_1_filename)
    train = train.dropna()

    # 전처리_3 -> 원핫 진행
    enc_arr = ['입찰월', '입찰일']
    enc_1.fit(train[enc_arr])
    enc_df = pd.DataFrame(data=enc_1.transform(train[enc_arr]).toarray(), columns=enc_1.get_feature_names(enc_arr),
                          dtype=bool)
    enc_df= enc_df.replace(True,1)
    enc_df = enc_df.replace(False, 0)
    train = pd.concat([train.drop(columns=enc_arr), enc_df], axis=1)
    train = train.dropna()
    one_hot_1_filename = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_enc_1.joblib"
    joblib.dump(enc_1, path + '/' + one_hot_1_filename)

    print('dong 모델 fit 전 정보')
    print(train.info())
    # 모델 fit
    X = train.drop(columns='예가율').copy()
    y = train['예가율'].copy()
    etr_1.fit(X, y)
    etr_1_filename = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_etr_1_model.joblib"
    joblib.dump(etr_1, path + '/' + etr_1_filename)
    print('success model fit _ dong ver')


    #test 시작

    base_cost = test['기초금액'].values[0]
    base_ratio = test['낙찰하한율'].values[0]

    test['입찰날짜'] = pd.to_datetime(test['입찰날짜'])
    test['발주청'] = test['발주청'].str.replace(' ', '')
    test['시도'] = test['시도'].str.replace(' ', '')
    test['입찰월'] = test['입찰날짜'].dt.month
    test['입찰일'] = test['입찰날짜'].dt.day
    test = test[['입찰월','입찰일','연면적','대지면적','세대수','기초금액','낙찰하한율']]
    # log 및 std 변환
    test[['std_연면적','std_대지면적','std_세대수','std_기초금액']] =scaler_1.transform(np.log1p(test[['연면적','대지면적','세대수','기초금액']]))
    test = test[['입찰월','입찰일','낙찰하한율','std_연면적','std_대지면적','std_세대수','std_기초금액']]
    # 다항회귀 변환
    poly_col_arr = ['std_연면적', 'std_대지면적', 'std_세대수', 'std_기초금액','낙찰하한율']

    pred_poly_df = pd.DataFrame(data=poly_1.transform(test[poly_col_arr]), columns=poly_1.get_feature_names(poly_col_arr))
    pred_poly = pd.concat([test.drop(columns=poly_col_arr), pred_poly_df], axis=1)
    # 원핫 변환
    enc_col_arr = ['입찰월','입찰일']
    print(enc_1.get_feature_names(enc_col_arr))
    pred_enc_df = pd.DataFrame(data=enc_1.transform(pred_poly[enc_col_arr]).toarray(), columns=enc_1.get_feature_names(enc_col_arr),dtype=bool)
    pred_enc_df= pred_enc_df.replace(True,1)
    pred_enc_df = pred_enc_df.replace(False, 0)
    pred_enc = pd.concat([pred_poly.drop(columns=enc_col_arr), pred_enc_df], axis=1)
    # 모델을 통한 예측하기
    pred_val = etr_1.predict(pred_enc)
    pred_cost = base_cost * base_ratio * pred_val
    st.session_state["dong_pred_ratio"] = pred_val
    st.session_state["dong_pred_value"] = pred_cost
    print('success pred dong ver')


def data_model(train,test):
    global enc_2, stack_reg2, path
    train = train.dropna()
    # 기본 변화 날짜변환, 형식변환
    train['입찰날짜'] = pd.to_datetime(train['입찰날짜'])
    train['발주청'] = train['발주청'].str.replace(' ', '')
    train['시도'] = train['시도'].str.replace(' ', '')
    train['입찰월'] = train['입찰날짜'].dt.month
    train['입찰일'] = train['입찰날짜'].dt.day
    train['입찰분기'] = train['입찰날짜'].dt.quarter

    train['예가율'] = train['예가율'].replace(',', '').astype(float)

    train = train[['예가율', '입찰월', '입찰일', '입찰분기', '시도', '발주청']]

    # 전처리_1 -> 원핫 진행
    enc_arr = ['입찰월', '입찰일', '입찰분기', '시도', '발주청']
    enc_2.fit(train[enc_arr])
    enc_df = pd.DataFrame(data=enc_2.transform(train[enc_arr]).toarray(), columns=enc_2.get_feature_names(enc_arr),
                          dtype=bool)
    enc_df= enc_df.replace(True,1)
    enc_df = enc_df.replace(False, 0)
    train = pd.concat([train.drop(columns=enc_arr), enc_df], axis=1)
    one_hot_2_filename = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_enc_2.joblib"
    joblib.dump(enc_2, path + '/' + one_hot_2_filename)

    # 모델 fit
    train = train.dropna().reset_index(drop=True)
    train2 = train.drop(columns = '예가율').astype(int)
    train2['예가율'] = train['예가율']

    X = train2.drop(columns='예가율').copy()
    y = train2['예가율'].copy()
    stack_reg2.fit(X, y)
    stack_reg2_file_name = datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분") + "_stack_reg2_model.joblib"
    joblib.dump(stack_reg2, path + '/' + stack_reg2_file_name)
    print('success model fit _ data ver')

    #test 시작

    base_cost = test['기초금액'].values[0]
    base_ratio = test['낙찰하한율'].values[0]

    test['입찰날짜'] = pd.to_datetime(test['입찰날짜'])
    test['발주청'] = test['발주청'].str.replace(' ', '')
    test['시도'] = test['시도'].str.replace(' ', '')
    test['입찰월'] = test['입찰날짜'].dt.month
    test['입찰일'] = test['입찰날짜'].dt.day
    test['입찰분기'] = test['입찰날짜'].dt.quarter
    test = test[['입찰월','입찰일','입찰분기','시도','발주청']]

    # 원핫 변환
    enc_col_arr = ['입찰월', '입찰일', '입찰분기', '시도', '발주청']
    print(enc_2.get_feature_names(enc_col_arr))
    pred_enc_df = pd.DataFrame(data=enc_2.transform(test[enc_col_arr]).toarray(), columns=enc_2.get_feature_names(enc_col_arr),dtype=bool)
    pred_enc_df= pred_enc_df.replace(True,1)
    pred_enc_df = pred_enc_df.replace(False, 0)
    pred_enc = pd.concat([test.drop(columns=enc_col_arr), pred_enc_df], axis=1)
    # 모델을 통한 예측하기
    pred_val = stack_reg2.predict(pred_enc)
    pred_cost = base_cost * base_ratio * pred_val
    st.session_state["data_pred_ratio"] = pred_val
    st.session_state["data_pred_value"] = pred_cost
    print('success pred data ver')


def pred_dong_model(df):
    global etr_1, enc_1, scaler_1, poly_1
    # 전처리 및 파생변수 생성
    base_cost = new_df['기초금액'].values[0]
    base_ratio = new_df['낙찰하한율'].values[0]
    df['입찰날짜'] = pd.to_datetime(df['입찰날짜'])
    df['발주청'] = df['발주청'].str.replace(' ', '')
    df['시도'] = df['시도'].str.replace(' ', '')
    df['입찰월'] = df['입찰날짜'].dt.month
    df['입찰일'] = df['입찰날짜'].dt.day
    df = df[['입찰월','입찰일','연면적','대지면적','세대수','기초금액','낙찰하한율']]
    # log 및 std 변환
    df[['std_연면적','std_대지면적','std_세대수','std_기초금액']] =scaler_1.transform(np.log1p(df[['연면적','대지면적','세대수','기초금액']]))
    df = df[['입찰월','입찰일','낙찰하한율','std_연면적','std_대지면적','std_세대수','std_기초금액']]
    # 다항회귀 변환
    poly_col_arr = ['낙찰하한율','std_연면적', 'std_대지면적', 'std_세대수', 'std_기초금액']
    pred_poly_df = pd.DataFrame(data=poly_1.transform(df[poly_col_arr]), columns=poly_1.get_feature_names(poly_col_arr))
    pred_poly = pd.concat([df.drop(columns=poly_col_arr), pred_poly_df], axis=1)
    # 원핫 변환
    enc_col_arr = ['입찰일','입찰월']
    pred_enc_df = pd.DataFrame(data=enc_1.transform(pred_poly[enc_col_arr]).toarray(), columns=enc_1.get_feature_names(enc_col_arr),dtype=bool)
    pred_enc_df= pred_enc_df.replace(True,1)
    pred_enc_df = pred_enc_df.replace(False, 0)
    pred_enc = pd.concat([pred_poly.drop(columns=enc_col_arr), pred_enc_df], axis=1)
    # 모델을 통한 예측하기
    pred_val = etr_1.predict(pred_enc)
    pred_cost = base_cost * base_ratio * pred_val
    st.session_state["dong_pred_ratio"] = pred_val
    st.session_state["dong_pred_value"] = pred_cost



def pred_data_model(df):
    global enc_2, stack_reg2
    # 전처리 및 파생변수 생성
    base_cost = new_df['기초금액'].values[0]
    base_ratio = new_df['낙찰하한율'].values[0]
    df['입찰날짜'] = pd.to_datetime(df['입찰날짜'])
    df['발주청'] = df['발주청'].str.replace(' ', '')
    df['시도'] = df['시도'].str.replace(' ', '')
    df['입찰월'] = df['입찰날짜'].dt.month
    df['입찰일'] = df['입찰날짜'].dt.day
    df['입찰분기'] = df['입찰날짜'].dt.quarter
    df = df[['입찰월','입찰분기','입찰일','시도','발주청']]

    # 원핫 변환
    enc_col_arr = ['시도','발주청','입찰분기','입찰일','입찰월']
    pred_enc_df = pd.DataFrame(data=enc_2.transform(df[enc_col_arr]).toarray(), columns=enc_2.get_feature_names(enc_col_arr),dtype=bool)
    pred_enc_df= pred_enc_df.replace(True,1)
    pred_enc_df = pred_enc_df.replace(False, 0)
    pred_enc = pd.concat([df.drop(columns=enc_col_arr), pred_enc_df], axis=1)
    # 모델을 통한 예측하기
    pred_val = stack_reg2.predict(pred_enc)
    pred_cost = base_cost * base_ratio * pred_val
    st.session_state["data_pred_ratio"] = pred_val
    st.session_state["data_pred_value"] = pred_cost











# def 함수 선언하는 곳 끝
# ---------------------------------#



# ---------------------------------#
# 예측한 예가율 및 계산된금액 미리 선언
if 'dong_pred_ratio' not in st.session_state:
    st.session_state["dong_pred_ratio"] = 0
if 'dong_pred_value' not in st.session_state:
    st.session_state["dong_pred_value"] = 0
if 'data_pred_ratio' not in st.session_state:
    st.session_state["data_pred_ratio"] = 0
if 'data_pred_value' not in st.session_state:
    st.session_state["data_pred_value"] = 0
if 'euclide_df' not in st.session_state:
    st.session_state['euclide_df'] = pd.DataFrame(columns=['공고번호', '낙찰하한율', '연면적', '대지면적', '기초금액', '예가율_dong', '예가율_data'])

# ---------------------------------#
st.write("""
# 머신러닝을 통한 입찰분석
""")

# ---------------------------------#
# Sidebar - Collects user input features into dataframe

with st.sidebar.header('0. Select CSV or Model'):
    pages = ['기본(22년7월)','학습데이터 입력 및 예측',"최종 학습일 지정(모델읽어오기)"]

    page = st.sidebar.radio("Navigate", options=pages)
    st.title(page)
    if page == "기본(22년7월)":
        st.sidebar.header('22년 7월까지 학습된 데이터로 진행합니다')
        st.download_button(
            label="22년 7월까지의 기초 자료 다운",
            data = pd.read_csv('./base_model/최종모델기초데이터.csv',encoding = 'cp949').to_csv().encode('utf-8'),
            file_name= '기초데이터_21년7월.csv',
            mime='text/csv'
        )

    elif page == "최종 학습일 지정(모델읽어오기)":
        with st.sidebar.header('예측 모델(최종학습날짜)을 선택해주세요'):
            model_list = glob.glob('./model/*',  recursive = True)
            for i in range(len(model_list)):
                model_list[i] = model_list[i].split('/')[2]
            model_value = st.selectbox("모델 선택 ", model_list)

    elif page == "학습데이터 입력 및 예측":
        st.sidebar.header('학습시킬 데이터를 업로드해주세요')
        st.sidebar.header("데이터 업로드 양식은 기본(22년 7월)에 나타나있는 기초데이터 양식을 활용해 주세요")
        uploaded_file = st.sidebar.file_uploader("학습시킬 데이터(CSV)를 업로드해주세요", type=["csv"])




    # Sidebar - Specify parameter settings
    with st.sidebar.subheader('예측자료 입력'):
        date_1 = st.date_input("2. 공고날짜를 입력해주세요", value=datetime.date(2022, 8, 15),
                               min_value=datetime.date(2012, 1, 1),
                               max_value=datetime.date(2022, 12, 31))
    with st.sidebar.subheader('예측자료 입력'):
        date_2 = st.date_input("3. 낙찰날짜를 입력해주세요", value=datetime.date(2022, 8, 17),
                               min_value=datetime.date(2012, 1, 1),
                               max_value=datetime.date(2022, 12, 31))
    with st.sidebar.subheader('예측자료 입력'):
        ratio_list = [0.8295, 0.8045, 0.7295, 0.8495]
        ratio_option = list(range(len(ratio_list)))
        ratio_value = st.selectbox("4. 낙찰하한율을 입력해주세요", ratio_option, format_func=lambda x: ratio_list[x])
    with st.sidebar.subheader('예측자료 입력'):
        client_list = ['경기도양주시', '충청남도홍성군', '경기도용인시', '대구광역시', '경기도의왕시', '경기도평택시',
                       '경상남도창원시', '부산광역시사상구', '전라북도군산시', '인천광역시경제자유구역청', '경기도이천시',
                       '제주특별자치도제주시', '서울특별시은평구', '서울특별시중랑구', '울산광역시남구', '부산광역시연제구',
                       '서울특별시강북구', '충청남도아산시', '전라남도장흥군', '대전광역시', '인천광역시계양구', '경기도화성시',
                       '충청남도예산군', '서울특별시동작구', '강원도강릉시', '인천광역시서구', '강원도속초시', '경기도수원시',
                       '경기도부천시', '서울특별시용산구', '강원도원주시', '경기도의정부시', '경상북도포항시', '충청남도천안시',
                       '서울특별시관악구', '경기도오산시', '경상남도양산시', '전라북도익산시', '경기도성남시', '경상남도김해시',
                       '충청북도진천군', '서울특별시영등포구', '대구광역시남구', '울산광역시', '충청북도청주시', '전라남도영암군',
                       '인천광역시연수구', '제주특별자치도서귀포시', '부산광역시남구', '서울특별시광진구', '대구광역시수성구',
                       '경상남도사천시', '인천광역시미추홀구', '서울특별시서초구', '경상북도구미시', '충청북도음성군', '경기도파주시',
                       '대전광역시동구', '서울특별시성북구', '충청북도충북경제자유구역청', '부산광역시', '광주광역시광산구',
                       '경상북도경산시', '대전광역시중구', '충청북도옥천군', '경상북도칠곡군', '전라남도무안군', '부산광역시동래구',
                       '전라북도김제시', '경상북도김천시', '경기도광명시', '인천광역시동구', '경기도안성시', '강원도양양군',
                       '경기도양평군', '부산광역시북구', '전라남도화순군', '서울특별시강서구', '인천광역시남동구', '서울특별시금천구',
                       '인천광역시동구청', '서울특별시구로구', '강원도춘천시', '전라남도광양시', '경기도광주시', '전라남도고흥군',
                       '충청남도당진시', '경기도동두천시', '부산광역시해운대구', '충청북도제천시', '광주광역시남구', '경상남도거창군',
                       '경상북도울진군', '서울특별시송파구', '서울특별시강남구', '전라북도전주시', '인천광역시부평구',
                       '전라남도여수시', '부산광역시부산진구', '부산광역시사하구', '부산광역시서구', '충청북도충주시',
                       '전라남도담양군', '경상남도진주시', '전라남도순천시', '경기도가평군', '서울특별시마포구', '경상남도남해군',
                       '광주광역시북구', '서울특별시동대문구', '광주광역시동구', '대구광역시달성군', '경기도연천군',
                       '울산광역시울산경제자유구역청', '울산광역시울주군', '전라남도곡성군', '대구광역시중구', '서울특별시',
                       '전라남도장성군', '전라북도완주군', '서울특별시성동구', '경상북도경주시', '서울특별시노원구',
                       '대구광역시달서구', '충청남도서천군', '대전광역시대덕구', '강원도평창군', '부산광역시기장군', '경기도고양시',
                       '경기도남양주시', '전라북도무주군', '경상남도거제시', '전라남도영광군', '경상남도통영시', '광주광역시서구',
                       '세종특별자치시', '울산광역시중구', '제주특별자치도', '경기도시흥시', '경기도구리시', '경기도안산시',
                       '강원도홍천군', '대구광역시북구', '서울특별시강동구', '전라남도목포시', '강원도철원군', '서울특별시송파구청',
                       '경기도안양시', '전라남도구례군', '대구경북경제자유구역청', '대전광역시서구', '전라북도남원시',
                       '부산광역시강서구', '경기도김포시', '충청남도공주시', '충청남도논산시', '대구광역시서구', '경상북도안동시',
                       '경기도포천시', '전라남도신안군', '경기도여주시', '전라남도나주시', '강원도동해시', '서울특별시서대문구',
                       '경상남도하동군', '경기도하남시', '충청남도서산시', '인천광역시중구', '경상북도성주군', '대구광역시동구',
                       '서울특별시양천구', '부산.진해경제자유구역청', '강원도삼척시', '충청남도계룡시', '충청북도단양군',
                       '충청남도금산군', '부산광역시영도구', '경상남도밀양시', '인천광역시강화군', '부산광역시수영구', '경기도과천시',
                       '경상남도함안군', '서울특별시중구', '충청북도증평군', '부산광역시동구', '울산광역시동구',
                       '행정중심복합도시건설청', '강원도횡성군', '경상북도영주시', '강원도영월군', '대전광역시유성구',
                       '경상북도영천시', '강원도고성군', '경기도군포시', '충청남도보령시', '부산광역시금정구', '강원도태백시',
                       '전라북도부안군', '울산광역시북구', '전라남도해남군', '광양만권경제자유구역청', '광주광역시', '경상남도의령군',
                       '경상북도고령군', '경상남도고성군', '경상북도예천군', '충청남도부여군', '경상북도상주시', '전라북도정읍시',
                       '충청남도태안군', '전라북도', '서울특별시종로구', '충청북도청주시청원구', '경상남도창녕군', '경상북도영덕군']
        client_option = list(range(len(client_list)))
        client_value = st.selectbox("05. 발주청을 선택하세요", client_option, format_func=lambda x: client_list[x])
    with st.sidebar.subheader('예측자료 입력'):
        sido_list = ['경기도', '충청남도', '대구광역시', '경상남도', '부산광역시', '전라북도', '인천광역시', '제주특별자치도', '서울특별시', '울산광역시', '전라남도',
                     '대전광역시', '강원도', '경상북도',
                     '충청북도', '광주광역시', '세종특별자치시']
        sido_option = list(range(len(sido_list)))
        sido_value = st.selectbox("06. 시도를선택하세요", sido_option, format_func=lambda x: sido_list[x])
    with st.sidebar.subheader('7. 대지면적을 입력해주세요'):
        land_area = st.text_input("7. 대지면적을 입력해주세요")
    with st.sidebar.subheader('8. 연면적을 입력해주세요'):
        build_area = st.text_input("8. 연면적을 입력해주세요")
    with st.sidebar.subheader('9. 기초금액을 입력해주세요'):
        cost = st.text_input("9. 기초금액을 입력해주세요")
    with st.sidebar.subheader('10. 세대수를 입력해주세요'):
        household = st.text_input("10. 세대수를 입력해주세요")
    with st.sidebar.subheader('Predict Button'):
        if st.button('Show prediction'):
            new_data = {
                    '공고날짜': [date_1],'입찰날짜': [date_2],'낙찰하한율': [ratio_list[ratio_value]],
                '발주청': [client_list[client_value]],'시도': [sido_list[sido_value]],
                '연면적': [land_area],'대지면적': [build_area],'기초금액': [cost],'세대수':[household]}
            new_df = pd.DataFrame(new_data)
            new_df['세대수'] = new_df['세대수'].astype(float)
            new_df['기초금액'] = new_df['기초금액'].astype(float)
            new_df['대지면적'] = new_df['대지면적'].astype(float)
            new_df['연면적'] = new_df['연면적'].astype(float)
            if page == "기본(22년7월)":
                etr_1 = joblib.load(glob.glob('./base_model/base_etr_1_model.joblib')[0])
                enc_1 = joblib.load(glob.glob('./base_model/base_onehot_1.joblib')[0])
                scaler_1 = joblib.load(glob.glob('./base_model/base_scaler_1.save')[0])
                poly_1 = joblib.load(glob.glob('./base_model/base_poly_1.joblib')[0])

                enc_2 = joblib.load(glob.glob('./base_model/base_onehot_2.joblib')[0])
                stack_reg2 = joblib.load(glob.glob('./base_model/base_stack_reg2_model.joblib')[0])

                pred_dong_model(new_df)
                pred_data_model(new_df)


            elif page == "최종 학습일 지정(모델읽어오기)" :
                etr =joblib.loac(glob.glob('./'+model_value+'/*etr_1_model.joblib')[0])
                enc_1 = joblib.loac(glob.glob('./'+model_value+'/*onehot_1.joblib')[0])
                scaler_1 = joblib.loac(glob.glob('./'+model_value+'/*scaler_1.joblib')[0])
                poly_1 = joblib.loac(glob.glob('./'+model_value+'/*poly_1.joblib')[0])

                enc_2 = joblib.loac(glob.glob('./'+model_value+'/*obehot_2.joblib')[0])
                stack_reg2 = joblib.loac(glob.glob('./'+model_value+'/*stacke_reg2_model.joblib')[0])

                pred_dong_model(new_df)
                pred_data_model(new_df)

            elif page == '학습데이터 입력 및 예측':
                os.mkdir('./model/'+datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분"))
                path = './model/'+datetime.datetime.today().strftime("%Y년_%m월_%d일_%H시_%M분")
                train = pd.read_csv(uploaded_file, encoding = 'utf-8')
                dong_model(train,new_df)
                data_model(train,new_df)





            st.session_state['euclide_df'] = pd.DataFrame(columns=['공고번호', '낙찰하한율', '연면적', '대지면적', '기초금액', '예가율_dong', '예가율_data'])
            st.session_state['euclide_df'] = st.session_state['euclide_df'].append({'공고번호': 9999, '낙찰하한율': ratio_list[ratio_value], '연면적': land_area, '대지면적': build_area, '기초금액': cost,
                                                                                    '예가율_dong': st.session_state["dong_pred_ratio"]*100,'예가율_data': st.session_state["data_pred_ratio"]*100}, ignore_index=True)

            new_euclidean = st.session_state['euclide_df'].astype(float)
            new_concat = st.session_state['concat_df'][['공고번호', '연면적', '대지면적', '기초금액', '낙찰하한율', '예가율']]
            new_result = pd.concat([new_euclidean,new_concat])
            result_euclidean = pd.DataFrame(squareform(pdist(new_result.iloc[:, 1:])), columns=new_result['공고번호'].unique(),index=new_result['공고번호'].unique())
            list_e = list(result_euclidean.loc[9999].sort_values().head(10).index)
            st.session_state['result'] = st.session_state['concat_df'][st.session_state['concat_df']['공고번호'].isin(list_e)][['공고번호', '입찰날짜', '연면적', '대지면적', '기초금액', '낙찰하한율', '예가율']].reset_index(drop = True)
            st.session_state['result'] = st.session_state['result'].astype({"연면적": int,"대지면적": int,"기초금액": int}, errors='raise')
            # print('예측한 투찰율 : {:0,.4f}%'.format(float(pred_val) * 100))
                # print('예측한 계산된 가격 : {0:,}'.format(int(pred_cost)))
                # print('End Sequence!!!!!!!!!!!!')


# ---------------------------------#
# Main panel

# Displays the dataset
st.header('1. 예측하기')

st.table(st.session_state['euclide_df'])

st.write('Dong_ver 예측_예가율 및 계산가격 ')
# 초록색을 사용하기위해 success 를 사용
st.success('{:0,.4f}%'.format(float(st.session_state["dong_pred_ratio"]) * 100))
st.success('{0:,}'.format(int(st.session_state["dong_pred_value"])))

st.write('Data_ver 예측_예가율 및 계산가격 ')
# 노란색을 사용하기위해 warning 을 사용
st.warning('{:0,.4f}%'.format(float(st.session_state["data_pred_ratio"]) * 100))
st.warning('{0:,}'.format(int(st.session_state["data_pred_value"])))
#

st.header('2. 타기업 분석 ')

option = st.selectbox(
    '기업리스트',
    ('(주)케이디엔지니어링건축사사무소', '(주)토펙엔지니어링건축사사무소', '(주)토문엔지니어링 건축사사무소',
     '주식회사 아이티엠코퍼레이션건축사사무소', '(주)한림이앤씨건축사사무소', '(주)태원종합기술단건축사사무소',
     '(주)한국종합건축사사무소', '(자)건축사사무소 태백', '주식회사 동우이앤씨', '주식회사 영화키스톤건축사사무소'))

if st.button("타기업 분석"):
    st.subheader(option + ' 기업 분석 - 전체')
    test_plt = pd.read_csv('./기업분석_전체/' + option + '_prophet.csv')
    test_plt = test_plt.iloc[:-100, :]
    figsize = (10, 6)
    xlabel = 'ds'
    ylabel = 'y'
    test_plt['ds'] = pd.to_datetime(test_plt['ds'], errors='coerce')
    fig = plt.figure(facecolor='w', figsize=figsize)
    ax = fig.add_subplot(111)
    fcst_t = test_plt['ds'].dt.to_pydatetime()
    ax.plot(test_plt['ds'].dt.to_pydatetime(), test_plt['y'], 'k.')
    ax.plot(fcst_t, test_plt['yhat_' + option], ls='-', c='#0072B2')
    ax.fill_between(fcst_t, test_plt['yhat_lower'], test_plt['yhat_upper'], color='#0072B2', alpha=0.2)
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()
    st.pyplot(fig)

    st.subheader(option + ' 기업 분석 - 2021년이후')
    test_plt = pd.read_csv('./기업분석_21년이후/' + option + '_prophet.csv')
    test_plt = test_plt.iloc[:-100, :]
    figsize = (10, 6)
    xlabel = 'ds'
    ylabel = 'y'
    test_plt['ds'] = pd.to_datetime(test_plt['ds'], errors='coerce')
    fig = plt.figure(facecolor='w', figsize=figsize)
    ax = fig.add_subplot(111)
    fcst_t = test_plt['ds'].dt.to_pydatetime()
    ax.plot(test_plt['ds'].dt.to_pydatetime(), test_plt['y'], 'k.')
    ax.plot(fcst_t, test_plt['yhat_' + option], ls='-', c='#0072B2')
    ax.fill_between(fcst_t, test_plt['yhat_lower'], test_plt['yhat_upper'], color='#0072B2', alpha=0.2)
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.tight_layout()
    st.pyplot(fig)

st.header('3. 유사공고 분석 ')


if 'concat_df' not in st.session_state:
    st.session_state['concat_df'] = pd.read_csv('./euclidean/euclidean.csv')#[['공고번호', '낙찰하한율', '연면적', '대지면적', '기초금액', '예가율']]

if 'result' not in st.session_state:
    st.session_state['result'] = pd.DataFrame()

if st.button('유사공고 확인하기'):
    st.subheader('입력한 데이터 예측값')
    st.table(st.session_state['euclide_df'])
    st.write('예측_예가율 Dong Ver ')
    # 초록색을 사용하기위해 success 를 사용
    st.success('{:0,.4f}%'.format(float(st.session_state["dong_pred_ratio"]) * 100))
    st.write('예측_예가율 Data Ver')
    st.warning('{:0,.4f}%'.format(float(st.session_state["data_pred_ratio"]) * 100))
    st.subheader('유사공고 기업 분석(1순위일수록 유사한 공고입니다)')
    st.table(st.session_state['result'])




footer="""<style>

.footer {

left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: right;
}
</style>
<div class="footer">
<p>Developed with 데이터청년캠퍼스 D1 Team<a style='display: block; font-size : 12px ; text-align: right;' </a></p>
<p>Developer : 전성현 신채현 이다희 조나현 <a style='display: block; font-size : 12px ; text-align: right;' </a></p>
<p>Developer Contact(전성현) : pengping@kakao.com , 010-4724-0871 <a style='display: block; font-size : 12px ; text-align: right;' </a></p>

</div>
"""
st.markdown(footer,unsafe_allow_html=True)