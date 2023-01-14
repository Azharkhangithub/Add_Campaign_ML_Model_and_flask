import pickle
import numpy as np
import pandas as pd
lr = pickle.load(open("model_age.pkl","rb"))
input_data = pickle.load(open("test_data.pkl","rb"))


from flask import Flask,request,render_template
app =Flask(__name__)



@app.route('/', methods=("POST","GET"))
def predict():
    # Columns or Features accepted by model for evaluation
    testData = input_data.loc[:, ['event_id','group_train', 'device_id', 'day', 'hour',
       'day_name', 'phone_brand', 'device_model', 'app_id', 'is_active',
       'label_id', 'category', 'count_events_perday', 'lat_median',
       'long_median', 'cluster']]
    unique_data = testData.groupby('device_id').head(1).reset_index(drop=True)
    fifty_device_id_data = unique_data.head(50)
    Xtest_dict = fifty_device_id_data.to_dict(orient='records')
    y_pred_final = lr.predict(Xtest_dict)
    df_predict = pd.DataFrame(y_pred_final.round(2), columns = ['age_predict'])
    result = pd.concat([fifty_device_id_data, df_predict], axis=1)
    # Drop unwanted columns
    result.drop(['event_id', 'group_train', 'day', 'hour', 'day_name',
       'phone_brand', 'device_model', 'app_id', 'is_active', 'label_id',
       'category', 'count_events_perday', 'lat_median', 'long_median',
       'cluster'], axis = 1, inplace = True)
    bins= [0,23,33,100]
    offer_labels = ['Bundled smartphone offers','payment wallet offers','cashback offers for Privilege Membership']
    campaigns_labels =['campaign-4','campaign-5','campaign-6']
    result['Campaign - Offers'] = pd.cut(result['age_predict'], bins=bins, labels=offer_labels, right=False)
    result['Campaign'] = pd.cut(result['age_predict'], bins=bins, labels=campaigns_labels, right=False)
    result.drop(['age_predict'], axis = 1, inplace = True)
    return render_template('index.html',  tables=[result.to_html(classes='data')], titles=result.columns.values)
    
    
    
    
if __name__=="__main__":
    app.run(port=5000,debug=True)