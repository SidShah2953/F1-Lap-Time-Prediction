def quantize_time(df,
                  time_col='Time'):
    df[time_col + 'Quant'] = (df[time_col] * 10**5 // 60).astype(int)

    return df