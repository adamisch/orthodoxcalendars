oca = pd.read_csv(
    "https://raw.githubusercontent.com/adamisch/orthodoxcalendars/main/oca_files/calendaroca.csv")

oca.replace({'Matt. ': 'Matthew ', 'Gal ': 'Galatians ',
             ";": ","}, inplace=True, regex=True)
oca.replace({np.nan: None}, inplace=True)

# Currently different days are on different rows
oca['Day'] = pd.to_datetime(oca['Day'])
oca = oca.groupby('Day').agg(list).sum(axis=1)
oca = oca.apply(lambda el: [x for x in el if pd.notna(x)])
oca = pd.DataFrame(oca)
oca = pd.DataFrame(oca[0].values.tolist(),
                   index=oca.index.strftime("%B %d, %Y"))

oca.rename(dict(zip(range(0, 10), ['Reading'+str(x) for x in range(1, 11)])),
           axis=1, inplace=True)

### Work in progress ###
oca=text.text_columns(oca, key = key, bible = kjv)
### end work in progress ###

cal_df_oca = copy.deepcopy(oca).reset_index()

cal_df_oca = cal_df_oca[['Day', 'Reading1', 'Text1', 'Reading2', 'Text2',
                         'Reading3', 'Text3', 'Reading4', 'Text4', 'Reading5',
                         'Text5', 'Reading6', 'Text6', 'Reading7', 'Text7',
                         'Reading8', 'Text8', 'Reading9', 'Text9', 'Reading10', 'Text10']]


cal_df_oca = cal_df_oca.stack().reset_index()
cal_df_oca = cal_df_oca[cal_df_oca[0] != " "]
