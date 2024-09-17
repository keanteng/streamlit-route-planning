# Streamlit Route Planning

Route planning application powered by `openrouteservice` and build with Streamlit. My original source code in Jupyter Notebook is [here](https://github.com/keanteng/travelling-salesman). You will need to create an API key at [`openrouteservice`](https://openrouteservice.org/) to use the application. 

## Use This Repo

Clone locally:
```bash
git clone https://github.com/keanteng/streamlit-route-planning
```

Install the dependencies:
```bash
py pip install -r requirements.txt
```

To run:
```bash
py -m streamlit run app.py
```

## File Structure

```
.
├── backend //functions and etc.
├── pages //app pages
└── app.py
```

## Use Case

Akmal is the boss of a goods trading company has he has a fleet of 5 vehicles. 
The company is based in Kamunting, Larut Matang, Perak and they will supply
goods to shops, wholesalers, and supermarkets in the northern Perak region. In the past,
the route planning will be done by his vehicles drivers and it is not efficient. Basically, 
the drivers will get the delivery location list from Akmal and they will plan the route. However, 
for new drivers or drivers who are not familiar with the area, they will take a longer time to plan the route.
And worse, sometimes when the drivers are absent or sick, the route planning will be delayed.

## Solution

With the help of technology, this project help Akmal to digitally plan the route for the shops
that he need to supply in a day. The project will tell:

- Which shop to deliver first for a given vehicle
- The time taken to deliver all the goods for a given vehicle

Of course, the project will take into account of situation such as shop opening time, and vehicle
capacity.