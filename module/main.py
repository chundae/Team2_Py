from data_loader import load_and_preprocess_data
from data_filter import filter_data
from data_resample import resample_data
from visualizer import plot_multiple_series, plot_single_series
from matplotlib import font_manager, rc


# 폰트 설정
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


# 메인 함수
# 메인 함수
def main(file_path, start_date, end_date, currency, frequency):
    # 파라미터 : 파일경로, 시작일, 종료일, 통화 종류, 분류 기간
    set_font()

    # 1. 데이터 불러오기
    data = load_and_preprocess_data(file_path)

    # 2. 통화 선택 및 필터링
    if currency == 'JPY':
        currency_columns = ['원/일본엔(100엔)']
    elif currency == 'USD':
        currency_columns = ['원/미국달러(매매기준율)']
    elif currency == 'ALL':
        currency_columns = data.columns
    else:
        raise ValueError("지원하지 않는 통화입니다. 'JPY', 'USD' 또는 'ALL'을 선택하세요.")

    # 3. 입력값으로 통화 / 시작,종료일 을 입력 받아 Filter으로 전송 후 반환 값을 할당
    filtered_data = filter_data(data, currency_columns, start_date, end_date) # 반환 값은 입력받은 통화 및 시작 ~ 종료일자로 받은 상태

    # 4. 데이터 분류(분리 기간 - 연단위/분기단위) -> 1차분류(시작/종료, 통화) 가 끝난 데이터를 한번더 분리하는 분류 기간을 선택
    if frequency == 'A':
        resampled_data = resample_data(filtered_data, 'Y')  # 연 단위
    elif frequency == 'Q':
        resampled_data = resample_data(filtered_data, 'Q')  # 분기 단위
    else:
        raise ValueError("지원하지 않는 분류 단위입니다. 'A' (연단위) 또는 'Q' (분기단위)를 선택하세요.")

    # 5. 그래프 출력 시각화 : 통화를 전부 선택한 경와 아닌경우 분리  -> 2차분류(분류기간)이 완료된 데이터를 분리 ""조건 : 통화를 모두 선택한 경우 바로 분리""
    if currency == 'ALL':
        plot_multiple_series(resampled_data, title='환율 변동', xlabel='날짜', ylabel='환율')
    else:
        plot_single_series(resampled_data, column=currency_columns[0], title='환율 변동', xlabel='날짜', ylabel='환율')


# 프로그램 실행
if __name__ == "__main__":
    # 사용 데이터 파일 고정
    file_path = 'Exchange.csv'

    # 사용자 입력(시작/종료일, 통화 선택, 분류 단위 선택)
    start_date = input("시작 날짜를 입력하세요 (예: 1980-01-01): ")
    end_date = input("종료 날짜를 입력하세요 (예: 2024-06-30): ")
    currency = input("통화를 선택하세요 (JPY, USD, 또는 ALL): ")
    frequency = input("데이터 분류 단위를 선택하세요 (연단위: A, 분기단위: Q): ")

    main(file_path, start_date, end_date, currency, frequency)
