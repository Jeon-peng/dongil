import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.preprocessing import *
from sklearn.preprocessing import OneHotEncoder


import os
import datetime
import glob
# ---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='동일건축 프로젝트 By 데이터청년캠퍼스',
                   layout='wide')


# ---------------------------------#
# Model building
def build_model(train):
    train = train.drop(columns='예정가격')
    train = train.dropna(axis=0)
    # 숫자에 콤마(,)가 들어가 있어 Object 형식으로 읽음 -> 콤마(,)를 제거 후 실수형(float)으로 변환하는 작업
    train['연면적'] = train['연면적'].str.replace(',', '').astype(float)
    train['세대수'] = train['세대수'].str.replace(',', '').astype(float)
    train['대지면적'] = train['대지면적'].str.replace(',', '').astype(float)
    train['예가율'] = train['예가율'].replace(',', '').astype(float)
    train['중간값'] = train['중간값'].replace(',', '').astype(float)
    train['기초금액'] = train['기초금액'].str.replace(',', '').astype(float)

    train['BidOpenDateTime'] = pd.to_datetime(train['BidOpenDateTime'])
    train['입찰분기'] = train['BidOpenDateTime'].dt.quarter
    train['NoticeDate'] = pd.to_datetime(train['NoticeDate'])
    train['공고분기'] = train['NoticeDate'].dt.quarter
    train['발주청'] = train['발주청'].str.replace(' ', '')
    train['시도'] = train['시도'].str.replace(' ', '')
    train['입찰일연'] = train['입찰일연'].astype(int)
    train['입찰일월'] = train['입찰일월'].astype(int)
    train['입찰일일'] = train['입찰일일'].astype(int)
    train = train.rename(columns={'G2B공고번호': '공고번호'})
    train = train.rename(columns={'입찰일연': '입찰년'})
    train = train.rename(columns={'입찰일월': '입찰월'})
    train = train.rename(columns={'입찰일일': '입찰일'})
    train = train.rename(columns={'입찰일요일': '입찰요일'})
    train = train.rename(columns={'공고일연': '공고년'})
    train = train.rename(columns={'공고일월': '공고월'})
    train = train.rename(columns={'공고일일': '공고일'})
    train = train.rename(columns={'공고일요일(개선)': '공고요일'})
    train = train.rename(columns={'NoticeDate': '공고날짜'})
    train = train.rename(columns={'BidOpenDateTime': '입찰날짜'})
    train = train.rename(columns={'최신_1순위': '1순위예가율'})

    train["log_연면적"] = np.log1p(train["연면적"])
    train["log_대지면적"] = np.log1p(train["대지면적"])
    train["log_세대수"] = np.log1p(train["세대수"])
    train["log_기초금액"] = np.log1p(train["기초금액"])
    train = train.reset_index(drop=True)
    scaler = StandardScaler()

    scaler.fit(train[['log_연면적', 'log_대지면적', 'log_세대수', 'log_기초금액', '참여업체수']])
    data_scaled = scaler.transform(train[['log_연면적', 'log_대지면적', 'log_세대수', 'log_기초금액', '참여업체수']])
    scaled_df = pd.DataFrame(data_scaled,
                             columns=['std_log_연면적', 'std_log_대지면적', 'std_log_세대수', 'std_log_기초금액', 'std_참여업체수'])
    train['std_연면적'] = scaled_df['std_log_연면적']
    train['std_대지면적'] = scaled_df['std_log_대지면적']
    train['std_세대수'] = scaled_df['std_log_세대수']
    train['std_기초금액'] = scaled_df['std_log_기초금액']
    train['std_참여업체수'] = scaled_df['std_참여업체수']
    # train[['연면적', '대지면적', '세대수', '기초금액', 'log_연면적',	'log_대지면적'	,'log_세대수',	'log_기초금액',	'std_연면적',	'std_대지면적',	'std_세대수',	'std_기초금액','std_참여업체수']].describe()

    train['시도'] = train['시도'].str.replace(' ', '')
    train['발주청'] = train['발주청'].str.replace(' ', '')

    cols = ['공고번호', '예가율', '1순위예가율', '낙찰하한율', '발주청', '시도', '공고년', '공고월', '공고일', '공고요일', '입찰년', '입찰월', '입찰일', '입찰요일',
            'std_연면적', 'std_대지면적', 'std_세대수', 'std_기초금액']

    dataset = train[cols]
    # Data splitting
    oh_cols = ['낙찰하한율', '발주청', '시도', '공고년', '공고월', '공고일', '공고요일', '입찰년', '입찰월', '입찰일', '입찰요일']
    ohe = OneHotEncoder(sparse=False)
    train_ohe = ohe.fit_transform(dataset[oh_cols])
    model_data_1 = pd.concat([dataset.drop(columns=oh_cols), pd.DataFrame(train_ohe, columns=ohe.get_feature_names_out())], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(model_data_1.drop(columns=['공고번호','1순위예가율', '예가율']), model_data_1['예가율'],
                                                        test_size=0.2, random_state=1)

    reg = ExtraTreesRegressor()
    reg.fit(X_train, y_train)


# ---------------------------------#
pred_df = pd.DataFrame(columns = ['공고일','입찰일','낙찰하한율','발주청','시도','연면적','대지면적','기초금액'])
if 'pred_ratio' not in st.session_state:
  st.session_state["pred_ratio"] = 0
if 'pred_value' not in st.session_state:
  st.session_state["pred_value"] = 0
def predict_value(date_1,date_2,ratio_value,client_value,sido_value,land_area,build_area,cost) :
    # pred_val = pd.DataFrame(columns = ['공고일','입찰일','낙찰하한율','발주청','시도','연면적','대지면적','기초금액'])
    global pred_df

    new_data = {
        '공고일': [date_1],
        '입찰일': [date_2],
        '낙찰하한율': [ratio_list[ratio_value]],
        '발주청': [client_list[client_value]],
        '시도': [sido_list[sido_value]],
        '연면적': [land_area],
        '대지면적': [build_area],
        '기초금액': [cost],
    }
    new_df = pd.DataFrame(new_data)
    pred_df = pd.concat([pred_df,new_df], axis = 0)

    st.session_state["pred_ratio"] = '99.554%'
    st.session_state["pred_value"] = '184,341,444원'

# """
# date_1 : 공고일
# date_2 : 입찰일
# ratio_value : 낙찰하한율
# clinet_value : 발주청
# sido_value : 시도
# land_area : 연면적
# build_area : 대지면적
# cost : 기초금액
# """


# ---------------------------------#
st.write("""
# 수주확대를 위한 머신러닝을 통한 입찰분석
동일건축 주택법 입력해야 할 값 : 공고일시, 입찰일시, 연면적, 대지면적, 기초금액, 낙찰하한율, 발주청, 시도
""")

# ---------------------------------#
# Sidebar - Collects user input features into dataframe

with st.sidebar.header('0. Select CSV or Model'):
    pages = ["CSV", "Model"]
    tags = ["Awesome", "Social"]

    page = st.sidebar.radio("Navigate", options=pages)
    st.title(page)
    if page == "CSV":
        with st.sidebar.header('1. 학습시킬 데이터를 업로드해주세요'):
            uploaded_file = st.sidebar.file_uploader("학습시킬 데이터(CSV)를 업로드해주세요", type=["csv"])
    else :
        with st.sidebar.header('예측 모델을 선택해주세요'):

            model_list = glob.glob(os.getcwd() + "/*/", recursive = True)
            uploaded_file = './입찰데이터_수정용_0804.csv'

            model_value = st.selectbox("모델 선택 ", model_list, format_func=lambda x: model_list[x])


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
    ratio_list =[0.8295, 0.8045, 0.7295, 0.8495]
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
    sido_list = ['경기도', '충청남도', '대구광역시', '경상남도', '부산광역시', '전라북도', '인천광역시','제주특별자치도', '서울특별시', '울산광역시', '전라남도', '대전광역시', '강원도', '경상북도',
       '충청북도', '광주광역시', '세종특별자치시']
    sido_option = list(range(len(sido_list)))
    sido_value = st.selectbox("06. 시도를선택하세요", sido_option, format_func=lambda x: sido_list[x])

with st.sidebar.subheader('7. 대지면적을 입력해주세요'):
    land_area = st.text_input("7. 대지면적을 입력해주세요")

with st.sidebar.subheader('8. 연면적을 입력해주세요'):
    build_area = st.text_input("8. 연면적을 입력해주세요")

with st.sidebar.subheader('9. 기초금액을 입력해주세요'):
    cost = st.text_input("9. 기초금액을 입력해주세요")

with st.sidebar.subheader('Predict Button'):
    if st.button('Show prediction') :
        predict_value(date_1,date_2,ratio_value,client_value,sido_value,land_area,build_area,cost)


# ---------------------------------#
# Main panel

# Displays the dataset
st.subheader('1. 데이터셋')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. 업로드한 데이터 셋 입니다**')
    st.write(df)
    # build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        df = pd.read_csv('./입찰데이터_수정용_0804.csv', index_col=0)
        st.markdown('엑셀 초기자료입니다')
        st.write(df.head(5))

        # build_model(df)

st.subheader('2. 예측하기')
st.dataframe(pred_df)





pred_ratio = 0
pred_value = 0
result_ratio = st.write('예측_예가율 ')
# 초록색을 사용하기위해 success 를 사용
st.success(st.session_state["pred_ratio"])
result_value = st.write('예측_계산가격 ')
# 노란색을 사용하기위해 warning 을 사용
st.warning(st.session_state["pred_value"])


st.subheader('3. 과거 유사 공고')


