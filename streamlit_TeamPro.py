import streamlit as st
from data_loader import load_and_preprocess_data  # 데이터 로드 및 전처리 함수
from data_filter import filter_data  # 데이터 필터링 함수
from data_resample import resample_data  # 데이터 리샘플링 함수
from visualizer import plot_multiple_series, plot_single_series  # 시각화 함수
from Quarterly import process_exchange_data, plot_exchange_rate
from matplotlib import font_manager, rc  # 폰트 설정
from matplotlib import pyplot as plt
# '''
# 웹페이시 시작 코드
# streamlit run streamlit_TeamPro.py
# '''

st.set_page_config(layout="wide")
st.markdown("""
<style>
.st-ca st-af st-c7{
    width: 100%;
}
.svg-container {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title('Team2_Project')
# st.set_page_config(layout="wide")

currency = st.sidebar.selectbox('currency', ['USD/KRW', 'JPY/KRW', 'ALL'])
start_date = st.sidebar.date_input('Start Date', value=None, min_value=None, max_value=None)
end_date = st.sidebar.date_input('End Date', value=None, min_value=None, max_value=None)
frequency = st.sidebar.selectbox('frequency', ['quarterly', 'yearly'])

file_path = 'Exchange.csv'

def set_font():
    font_path = None
    for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
        if 'AppleGothic' in font or 'NanumGothic' in font:
            font_path = font
            break
    if font_path is None:
        raise FileNotFoundError("AppleGothic 또는 NanumGothic 폰트를 찾을 수 없습니다.")
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)

@st.cache_data
def data_load():
    data = load_and_preprocess_data(file_path)
    return data

def rundata(start_date, end_date, currency, frequency):
    set_font()
    data = data_load()

    if currency == 'USD/KRW':
        currency_columns = ['원/미국달러(매매기준율)']
    elif currency == 'JPY/KRW':
        currency_columns = ['원/일본엔(100엔)']
    elif currency == 'ALL':
        currency_columns = data.columns
    else:
        st.error("지원하지 않는 통화입니다.")
        return None

    filtered_data = filter_data(data, currency_columns, start_date, end_date)

    if frequency == 'quarterly':
        resampled_data = resample_data(filtered_data, 'Q')
    elif frequency == 'yearly':
        resampled_data = resample_data(filtered_data, 'Y')
    else:
        st.error("지원하지 않는 분류 기간입니다.")
        return None


    st.write("Resampled Data Shape:", resampled_data.shape)

    if currency == 'ALL':
        fig = plot_multiple_series(resampled_data, title='환율 변동', xlabel='날짜', ylabel='환율')
    else:
        fig = plot_single_series(resampled_data, column=currency_columns[0], title='환율 변동', xlabel='날짜', ylabel='환율')
    return fig


def detailData(start_date, end_date, currency):
    set_font()
    data = data_load()

    if currency == 'USD/KRW':
        currency_columns = ['원/미국달러(매매기준율)']
    elif currency == 'JPY/KRW':
        currency_columns = ['원/일본엔(100엔)']
    elif currency == 'ALL':
        currency_columns = data.columns.tolist()
    else:
        st.error("지원하지 않는 통화입니다.")
        return None

    filtered_data = filter_data(data, currency_columns, start_date, end_date)
    start_year = start_date.year
    end_year = end_date.year
    quarters, average_values = process_exchange_data(filtered_data, start_year, end_year, currency_columns)

    fig = plot_exchange_rate(quarters, average_values, start_year, end_year, currency_columns)  # 수정된 부분
    return fig



tab1, tab2 = st.tabs(['선택기간','상세보기'])

if st.sidebar.button('그래프 생성'):

    with tab1:
        plot = rundata(start_date, end_date, currency, frequency)
        if plot is not None:
            st.plotly_chart(plot, use_container_width=True)

    with tab2:
        plot = detailData(start_date, end_date, currency)
        if plot is not None:
            st.plotly_chart(plot, use_container_width=True)



