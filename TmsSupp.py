import pandas as pd
import plotly.express as px
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# قراءة ملفات Excel
clients_df = pd.read_excel('عملاء محلي.xlsx')
suppliers_df = pd.read_excel('موردين22.xlsx')

# تنظيف الأعمدة من الفراغات
clients_df.columns = clients_df.columns.str.strip()
suppliers_df.columns = suppliers_df.columns.str.strip()

# معالجة القيم الناقصة في الأعمدة الرقمية
clients_df['مدين'] = pd.to_numeric(clients_df['مدين'], errors='coerce').fillna(0)
clients_df['دائن'] = pd.to_numeric(clients_df['دائن'], errors='coerce').fillna(0)
suppliers_df['مدين'] = pd.to_numeric(suppliers_df['مدين'], errors='coerce').fillna(0)
suppliers_df['دائن'] = pd.to_numeric(suppliers_df['دائن'], errors='coerce').fillna(0)



# تطبيق الوظيفة على الأعمدة النصية في بيانات العملاء
clients_df['إسـم العميـــل'] = clients_df['إسـم العميـــل']

# تطبيق الوظيفة على الأعمدة النصية في بيانات الموردين
suppliers_df['إسـم العميـــل'] = suppliers_df['إسـم العميـــل']

# عرض البيانات في Streamlit
st.title('تحليل بيانات العملاء والموردين')

# شريط جانبي للفلاتر
st.sidebar.header('فلاتر البيانات')

# إضافة خيار "كل العملاء" و "كل الموردين" في الاختيار
client_options = ['كل العملاء'] + clients_df['إسـم العميـــل'].unique().tolist()
supplier_options = ['كل الموردين'] + suppliers_df['إسـم العميـــل'].unique().tolist()

# فلترة البيانات بناءً على العملاء والموردين
selected_client = st.sidebar.selectbox('اختر العميل', client_options)
selected_supplier = st.sidebar.selectbox('اختر المورد', supplier_options)

if selected_client == 'كل العملاء':
    filtered_clients_df = clients_df
else:
    filtered_clients_df = clients_df[clients_df['إسـم العميـــل'] == selected_client]

if selected_supplier == 'كل الموردين':
    filtered_suppliers_df = suppliers_df
else:
    filtered_suppliers_df = suppliers_df[suppliers_df['إسـم العميـــل'] == selected_supplier]

# عرض البيانات الأولية
st.header('بيانات العملاء')
st.write(filtered_clients_df)

st.header('بيانات الموردين')
st.write(filtered_suppliers_df)

# معلومات ووصف البيانات
st.subheader('معلومات العملاء')
st.write(filtered_clients_df.describe())

st.subheader('معلومات الموردين')
st.write(filtered_suppliers_df.describe())

# رسم التوزيعات باستخدام Plotly Express (مع التحقق من وجود بيانات كافية)
if len(filtered_clients_df) > 1:
    st.subheader('توزيع مدين للعملاء')
    fig1 = px.histogram(filtered_clients_df, x='مدين', color='العملة', nbins=50, marginal='rug', title='توزيع مدين للعملاء')
    st.plotly_chart(fig1)
else:
    st.write("لا توجد بيانات كافية لرسم توزيع مدين للعملاء")

if len(filtered_suppliers_df) > 1:
    st.subheader('توزيع مدين للموردين')
    fig2 = px.histogram(filtered_suppliers_df, x='مدين', color='العملة', nbins=50, marginal='rug', title='توزيع مدين للموردين')
    st.plotly_chart(fig2)
else:
    st.write("لا توجد بيانات كافية لرسم توزيع مدين للموردين")

# رسم خرائط الحرارة للعلاقات
clients_corr = filtered_clients_df.select_dtypes(include=['number']).corr()
suppliers_corr = filtered_suppliers_df.select_dtypes(include=['number']).corr()

st.subheader('مصفوفة الارتباط للعملاء')
fig3 = px.imshow(clients_corr, text_auto=True, aspect='auto', title='مصوفة الارتباط للعملاء')
st.plotly_chart(fig3)

st.subheader('مصفوفة الارتباط للموردين')
fig4 = px.imshow(suppliers_corr, text_auto=True, aspect='auto', title='مصوفة الارتباط للموردين')
st.plotly_chart(fig4)

# رسم المخططات الشريطية لأكثر العملاء مديونية
st.subheader('أكثر العملاء مديونية')
top_debt_clients = filtered_clients_df.nlargest(10, 'مدين')
fig5 = px.bar(top_debt_clients, x='إسـم العميـــل', y='مدين', color='مدين', title='أكثر العملاء مديونية')
st.plotly_chart(fig5)

# رسم المخططات الشريطية لأكثر الموردين مديونية
st.subheader('أكثر الموردين مديونية')
top_debt_suppliers = filtered_suppliers_df.nlargest(10, 'مدين')
fig6 = px.bar(top_debt_suppliers, x='إسـم العميـــل', y='مدين', color='مدين', title='أكثر الموردين مديونية')
st.plotly_chart(fig6)

# رسم الرسوم البيانية الدائرية للعملاء حسب اسمائهم
st.subheader('نسبة مدين العملاء حسب الأسماء')
fig7 = px.pie(filtered_clients_df, values='مدين', names='إسـم العميـــل', title='نسبة مدين العملاء حسب الأسماء')
st.plotly_chart(fig7)

# رسم الرسوم البيانية الدائرية للموردين حسب اسمائهم
st.subheader('نسبة مدين الموردين حسب الأسماء')
fig8 = px.pie(filtered_suppliers_df, values='مدين', names='إسـم العميـــل', title='نسبة مدين الموردين حسب الأسماء')
st.plotly_chart(fig8)

# رسم المخططات الشريطية لرصيد كل عميل
st.subheader('رصيد كل عميل')
filtered_clients_df['الرصيد'] = filtered_clients_df['مدين'] - filtered_clients_df['دائن']
fig9 = px.bar(filtered_clients_df, x='إسـم العميـــل', y='الرصيد', color='الرصيد', title='رصيد كل عميل')
st.plotly_chart(fig9)

# رسم المخططات الشريطية لرصيد كل مورد
st.subheader('رصيد كل مورد')
filtered_suppliers_df['الرصيد'] = filtered_suppliers_df['مدين'] - filtered_suppliers_df['دائن']
fig10 = px.bar(filtered_suppliers_df, x='إسـم العميـــل', y='الرصيد', color='الرصيد', title='رصيد كل مورد')
st.plotly_chart(fig10)
