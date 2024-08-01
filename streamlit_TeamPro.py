import streamlit as st
from pyparsing import empty
from data_loader import load_and_preprocess_data  # 데이터 로드 및 전처리 함수
from data_filter import filter_data  # 데이터 필터링 함수
from data_resample import resample_data  # 데이터 리샘플링 함수
from visualizer import plot_multiple_series, plot_single_series  # 시각화 함수
from Quarterly import process_exchange_data, plot_exchange_rate
from matplotlib import font_manager, rc  # 폰트 설정
from exchange_rate_extremes import top_10_max_exchange, top_10_min_exchange
st.set_page_config(layout="wide")


st.sidebar.title('Team2_Project')

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

def top_max_min_exchange(start_date, end_date, currency):
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

    top_10_max = top_10_max_exchange(filtered_data)
    top_10_min = top_10_min_exchange(filtered_data)

    # 10개 미만의 데이터 처리
    if top_10_max.shape[0] < 10:
        st.warning(f"최대값 데이터가 {top_10_max.shape[0]}개만 존재합니다.")
    if top_10_min.shape[0] < 10:
        st.warning(f"최소값 데이터가 {top_10_min.shape[0]}개만 존재합니다.")

    return top_10_max, top_10_min


tab1, tab2 = st.tabs(['선택기간','상세보기'])

if st.sidebar.button('그래프 생성'):

    with tab1:
        plot = rundata(start_date, end_date, currency, frequency)
        top_max, top_min = top_max_min_exchange(start_date, end_date, currency)
        if plot is not None:
            st.plotly_chart(plot, use_container_width=True)

        empty1, con2, con3, empty2 = st.columns([0.3, 1, 1, 0.3])

        with empty1:
            empty()
        with con2:
            st.subheader('Top 10 Max')
            st.dataframe(top_max.head(10))

        with con3:
            st.subheader('Top 10 Min')
            st.dataframe(top_min.head(10))
        with empty2:
            empty()

    with tab2:
        plot = detailData(start_date, end_date, currency)
        if plot is not None:
            st.plotly_chart(plot, use_container_width=True)



