from plotly import graph_objects as go
import pandas as pd
import streamlit as st

def non_zero_columns(row):
    '''
    Get the names of non zero columns for a given row
    '''
    return row.columns[(row != 0).values.tolist()[0]]

st.set_page_config(layout="wide") 
st.title('Plotly Funnel Chart Example')
st.markdown('Developed with :heart: by [Koba Khit](https://www.linkedin.com/in/kobakhit/)')




# editable datatable
df = pd.DataFrame(
    [
       {"City": "Montreal", "Website Visits": 120, "Downloads": 60, "Potential Customers":30,'Requested Price':20, 'Invoice Sent':0,'Finalized':0},
       {"City": "Toronto", "Website Visits": 100, "Downloads": 60, "Potential Customers":40,'Requested Price':30, 'Invoice Sent':20,'Finalized':0},
       {"City": "Vancouver", "Website Visits": 90, "Downloads": 70, "Potential Customers":50,'Requested Price':30, 'Invoice Sent':10,'Finalized':5},
   ]
).set_index(['City'])


# code
code = '''
from plotly import graph_objects as go

fig = go.Figure()

fig.add_trace(go.Funnel(
    name = 'Montreal',
    y = ["Website visit", "Downloads", "Potential customers", "Requested price"],
    x = [120, 60, 30, 20],
    textinfo = "value+percent initial"))

fig.add_trace(go.Funnel(
    name = 'Toronto',
    orientation = "h",
    y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"],
    x = [100, 60, 40, 30, 20],
    textposition = "inside",
    textinfo = "value+percent previous"))

fig.add_trace(go.Funnel(
    name = 'Vancouver',
    orientation = "h",
    y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent", "Finalized"],
    x = [90, 70, 50, 30, 10, 5],
    textposition = "outside",
    textinfo = "value+percent total"))
'''

# chart placeholder
chart = st.container()

ui = st.container()

with ui:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('## Editable Data')
        st.write('Edit values in below table and the chart will adjust.')
        edited_df = st.data_editor(df, use_container_width=True)
    with c2:
        st.markdown('## Code')
        st.write('Source: https://plotly.com/python/funnel-charts/')
        st.code(code, line_numbers=True)

# chart code
fig = go.Figure()

fig.add_trace(go.Funnel(
    name = edited_df.index[0],
    y = non_zero_columns(edited_df[edited_df.index == edited_df.index[0]]),
    x = edited_df.iloc[edited_df.index == edited_df.index[0], :][non_zero_columns(edited_df[edited_df.index == edited_df.index[0]])].values.tolist()[0],
    textinfo = "value+percent initial"))

fig.add_trace(go.Funnel(
    name = edited_df.index[1],
    orientation = "h",
    y = non_zero_columns(edited_df[edited_df.index == edited_df.index[1]]),
    x = edited_df.iloc[edited_df.index == edited_df.index[1], :][non_zero_columns(edited_df[edited_df.index == edited_df.index[1]])].values.tolist()[0],
    textposition = "inside",
    textinfo = "value+percent previous"))

fig.add_trace(go.Funnel(
    name = edited_df.index[2],
    orientation = "h",
    y = non_zero_columns(edited_df[edited_df.index == edited_df.index[2]]),
    x = edited_df.iloc[edited_df.index == edited_df.index[2], :][non_zero_columns(edited_df[edited_df.index == edited_df.index[2]])].values.tolist()[0],
    textposition = "outside",
    textinfo = "value+percent total"))

fig.update_layout(height = 800, 
    font=dict(size=18),
    yaxis = dict(tickfont = dict(size=20))
)

# chart display
with chart.columns([1,5,1])[1]:
    st.plotly_chart(fig, use_container_width = True)


# favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
# st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
