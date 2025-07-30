import streamlit as st
from PIL import Image
import random

def add_sidebar_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://github.com/tpfeeney/spirited-reviews/blob/main/srlogo.png?raw=true');
                background-repeat: no-repeat;
                background-position: 20px 20px;
                padding-top: 180px;
                background-size: 150px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_sidebar_logo()


# --- Top Section: General Text ---
st.title("About the Spirited Crew")
st.write("""
Welcome to spirited reviews, where our goal is honest reviews, bold takes and questionable wisdom. Take a look around and see a history of our reviews, learn about the reviews we've done, and find your spirited palate match. We hope you enjoy and this helps you stay spirited.""")

# --- Grid Layout: 2x2 ---
# Placeholder images — replace with your own paths or URLs
img1 = Image.open("Randy.png")
img2 = Image.open("Norm.png")
img3 = Image.open("Zach.png")
img4 = Image.open("Justin.png")

# Data for each grid cell
people = [
    {"title": "Randy (TheDoerofstuff)", "image": img1, "text": """Randy is awesome, more to come.
<div style='font-size:20px;'><u><b>5 Favorite pours:</b></u></span><br>
1) Malort <br>
2) Malort  <br>
3) Malort <br>
4) Malort <br>
5) Malort <br>
<div style='font-size:20px;'><u><b>Top 2 Favorite Spirits:</b></u></span><br>
Still figuring it out<br>
"""},
    {"title": "Norm (Mild Turkey)",
    "image": img2,
    "text": """Norm is a dedicated family man who has been married to his wife Ashley for 20 years. He shares his life with his two wonderful daughters and two semi-loyal girl dogs. He finds joy in global travel, experiencing new cultures, and is always ready for an outdoor adventure. When relaxing, he often finds himself savoring a hi-proof scotch or bourbon with a great cigar.

<div style='font-size:20px;'><u><b>5 Favorite pours:</b></u></span><br>
1) Parker’s Heritage Double Barreled Blend<br>
2) Signatory Vintage Glenallachie 11 yr Speyside Scotch<br>
3) Laphroaig Cairdeas Cask Favorites 10 yr<br>
4) Russell’s Reserve Private Single Barrels Picks<br>
5) Rare Character TKO Ryes<br>
<div style='font-size:20px;'><u><b>Top 2 Favorite Spirits:</b></u></span><br>
Bourbon/Scotch<br>
"""},
    {"title": "Zach (stat1c_zach)", "image": img3, "text": """Born in Alabama where the white oak grows tall and strong (or so I've been told). I went to Auburn University (War Eagle!), emerging as an Aerospace Engineer (somehow). I now find myself in the Defense Industry, where I navigate complex projects and, presumably, ensure things fly straight (or at least don't explode prematurely).

When I'm not orchestrating the defense of the nation, you might find me on the ice, broom in hand, strategically sliding stones in the sport of curling. My initiation into this surprisingly addictive sport was less about personal ambition and more about a non-committal response to a coworker's question quickly followed by an unceremonious team sign-up. That was back in 2018, and since then, I've managed to rack up over ten league championships. Who knew a casual "yes" could lead to so much competitive sweeping?

Off the ice, my passions tend to be a bit more... spirited. My preferences are for the rich depths of bourbon and the malty allure of Scotch with peat smoke. And speaking of smoke, I'm just beginning my journey into the world of cigars, though I've quickly learned my limits – attempting to smoke more than one in a single sitting is a direct route to a very unpleasant evening.

My palate is as adventurous as my career path. I'm a self-proclaimed foodie, with a particular fondness for Asian and Italian cuisine. My culinary explorations have taken me to some wild places, including the rather unique experience of sampling sea urchin gonads on toast at The Aviary in Chicago – a city that remains one of my absolute favorite culinary playgrounds. And when I'm not exploring new flavors, you can often find me in my own kitchen, happily whipping up some sweet treats. I love the simple joys of pies and cookies the most!
<div style='font-size:20px;'><u><b>5 Favorite pours:</b></u></span><br>
1) Parker's Heritage Double Barrel<br>
2) Jack Daniel's 2021 Coy Hill<br>
3) Russell's Reserve 15 Year <br>
4) King of Kentucky 2024<br>
5) Jack Daniel's 14 Year<br>
<div style='font-size:20px;'><u><b>Top 2 Favorite Spirits:</b></u></span><br>
Still figuring it out<br>
"""},
    {"title": "Justin (Justin)", "image": img4, "text": """I’m a collector of old flowers, Four Roses lover, and firm believer that rye whiskey is proof chaos can be distilled into something beautiful. Proud father of two beautiful, brilliant, occasionally chaos-powered daughters who teach me patience daily — sometimes against my will. Husband to an amazing, supportive wife of seven years who somehow makes it all look easy. I find meaning in good conversation, sharing unique bottles, and chasing the stories that live between the sips. Life’s a blend, and I'm here for the people who make it all worth sipping.
<div style='font-size:20px;'><u><b>5 Favorite pours:</b></u></span><br>
1) Booker's Rye<br>
2) Watch Hill Proper 20 Batch 2<br>
3) Russel's Reserve 15<br>
4) Parker's Heritage Double Barrel Blend<br>
5) Four Roses Father's Day 2024 16 Year OESV<br>
<div style='font-size:20px;'><u><b>Top 2 Favorite Spirits:</b></u></span><br>
Still figuring it out

"""},
]

# --- Randomize Order ---
random.shuffle(people)

# --- Render the 2x2 Grid ---
for row in range(2):
    cols = st.columns(2)
    for col_idx in range(2):
        idx = row * 2 + col_idx
        person = people[idx]
        with cols[col_idx]:
            st.markdown(f"#### {person['title']}")
            pic_col, txt_col = st.columns([1, 2])
            with pic_col:
                st.image(person["image"], use_container_width=True)
            with txt_col:
                st.markdown(person["text"], unsafe_allow_html=True)