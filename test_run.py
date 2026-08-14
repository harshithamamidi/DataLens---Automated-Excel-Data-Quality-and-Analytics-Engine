import pandas as pd
import main

if __name__ == '__main__':
    df = pd.DataFrame({'a':[1,2,None],'b':['x','y',None]})
    print('profile:', main.profile_data(df))
    print('remove_duplicates:', main.remove_duplicates(df))
    print('convert:', main.convert_data_types(df))
    mv = main.missing_value_chart(df)
    print('missing_chart_type:', type(mv))
    out = main.export_cleaned_data(df, 'test.csv')
    print('exported:', out)
