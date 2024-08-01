import pandas as pd


def top_10_max_exchange(filtered_data):

    #결과 저장
    results = {'Date' : [], 'Currency':[], 'Max Value' :[]}

    for currency in filtered_data.columns:
        top_10 = filtered_data[currency].nlargest(10)

        results['Date'].extend(top_10.index)
        results['Currency'].extend([currency] * len(top_10))
        results['Max Value'].extend(top_10.values)


    result_df = pd.DataFrame(results)
    result_df['Date'] = pd.to_datetime(result_df['Date']).dt.strftime('%Y-%m-%d')
    return result_df

# nsmallest
def top_10_min_exchange(filtered_data):

    results = {'Date' : [], 'Currency':[], 'Min Value' :[]}

    for currency in filtered_data.columns:
        top_10 = filtered_data[currency].nsmallest(10)
        results['Date'].extend(top_10.index)
        results['Currency'].extend([currency] * len(top_10))
        results['Min Value'].extend(top_10.values)

    result_df = pd.DataFrame(results)
    result_df['Date'] = pd.to_datetime(result_df['Date']).dt.strftime('%Y-%m-%d')
    return result_df
