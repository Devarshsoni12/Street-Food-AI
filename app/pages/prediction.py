# Prediction Page
import sys
import streamlit as st
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PIL import Image
import numpy as np
from datetime import datetime
import json

if 'db' not in dir():
    from src.database import Database
    db = Database()
    db.connect()

_CLASS_INDICES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'models', 'class_indices.json'
)

if os.path.exists(_CLASS_INDICES_PATH):
    with open(_CLASS_INDICES_PATH, 'r') as _f:
        _indices = json.load(_f)
    CLASS_NAMES = [k.replace('_', ' ') for k, v in sorted(_indices.items(), key=lambda x: x[1])]
else:
    CLASS_NAMES = [
        'Aloo Paratha', 'Burger', 'Chole Bhature', 'Dhokla', 'Dosa',
        'Grilled Sandwich', 'Idli', 'Medu Vada', 'Misal Pav', 'Momos',
        'Pakoda', 'Pani Puri', 'Pav Bhaji', 'Poha', 'Samosa',
        'Sev Puri', 'Unknown', 'Vada Pav'
    ]

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'models', 'food_classifier.h5'
)

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        import tensorflow as tf
        return tf.keras.models.load_model(MODEL_PATH)
    return None

model = load_model()

def predict_food(image):
    if model is None:
        return None, 0.0, False
    img = image.resize((224, 224))
    img_array = np.array(img.convert('RGB')) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array, verbose=0)
    idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][idx])
    food_name = CLASS_NAMES[idx]
    if food_name == 'Unknown' or confidence < 0.75:
        return 'Unknown', confidence, True
    return food_name, confidence, True

#  Rich food details lookup 
FOOD_DETAILS = {
    'Aloo Paratha': {
        'long_description': (
            "Aloo Paratha is one of the most beloved breakfast dishes of North India, especially Punjab. "
            "It is a thick, unleavened whole wheat flatbread stuffed with a spiced mashed potato filling. "
            "The dough is rolled out, filled with the potato mixture, sealed and rolled again, then cooked "
            "on a hot tawa (griddle) with generous amounts of butter or ghee. It is a hearty, filling dish "
            "that has been a staple in Indian households for centuries and is enjoyed by people of all ages."
        ),
        'ingredients': [
            'Whole wheat flour (atta)', 'Boiled & mashed potatoes', 'Green chillies',
            'Fresh coriander leaves', 'Cumin seeds', 'Garam masala', 'Amchur (dry mango powder)',
            'Salt', 'Butter / Ghee', 'Water (for dough)'
        ],
        'preparation': (
            "1. Knead whole wheat flour with water and salt into a soft dough; rest for 20 minutes. "
            "2. Mix mashed potatoes with chopped green chillies, coriander, cumin, garam masala, amchur and salt. "
            "3. Divide dough into balls, flatten each, place a spoonful of filling in the centre, seal the edges and roll gently into a flat disc. "
            "4. Cook on a hot tawa for 2-3 minutes per side, applying butter or ghee until golden brown spots appear."
        ),
        'serving_suggestions': (
            "Best served hot with a dollop of white butter, a bowl of fresh curd (yogurt), "
            "tangy mango pickle (aam ka achar), and a glass of chilled lassi on the side."
        ),
        'origin': 'Punjab, India',
        'history': (
            "Aloo Paratha has its roots in the Punjab region of the Indian subcontinent, where it has been "
            "a breakfast staple for hundreds of years. It gained widespread popularity across North India "
            "during the Mughal era and remains one of the most cherished comfort foods in Indian households today."
        ),
        'famous_for': {
            'city': 'Punjab',
            'text': (
                "Aloo Paratha is most famous in {city}, where it is served at every dhaba and household breakfast table. "
                "It is celebrated for its perfectly spiced potato filling wrapped in a crispy, buttery whole wheat crust — "
                "a dish that defines the warmth and richness of North Indian home cooking."
            ),
        },
    },
    'Burger': {
        'long_description': (
            "The Indian street-style burger is a delicious fusion of Western fast food and local flavours. "
            "A soft bun is loaded with a spiced vegetable or aloo tikki patty, fresh lettuce, tomato, onion rings, "
            "and slathered with mint chutney and tangy sauces. Street vendors across India have made it their own "
            "by adding chaat masala and local spices, giving it a uniquely desi twist that sets it apart from its Western counterpart."
        ),
        'ingredients': [
            'Burger bun', 'Aloo tikki / veg patty', 'Lettuce leaves', 'Tomato slices',
            'Onion rings', 'Cheese slice', 'Mint chutney', 'Tomato ketchup',
            'Mayonnaise', 'Chaat masala', 'Butter'
        ],
        'preparation': (
            "1. Prepare the patty by mixing boiled mashed potatoes with spices, breadcrumbs and herbs; shape and shallow fry until crispy. "
            "2. Slice the bun and lightly toast it on a griddle with butter. "
            "3. Spread mint chutney on the bottom bun, layer with lettuce, tomato, onion and the hot patty. "
            "4. Add cheese, drizzle ketchup and mayo, sprinkle chaat masala, and close with the top bun."
        ),
        'serving_suggestions': (
            "Serve immediately while the patty is hot and crispy, alongside masala fries or wafers "
            "and a cold drink or milkshake for a complete street-food experience."
        ),
        'origin': 'Mumbai, India (adapted from USA)',
        'history': (
            "The burger originated in the United States in the late 19th century but was reimagined by "
            "Indian street vendors in Mumbai and Delhi during the 1980s and 90s. Local adaptations using "
            "aloo tikki patties, mint chutney and chaat masala gave it a distinctly desi identity that "
            "made it a staple of Indian fast food culture."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "The Indian-style burger is most famous on the streets of {city}, where vendors reinvented "
                "the classic with aloo tikki patties, zesty mint chutney and chaat masala. "
                "It is loved for delivering bold desi flavours in every bite at an unbeatable street-side price."
            ),
        },
    },
    'Chole Bhature': {
        'long_description': (
            "Chole Bhature is a iconic North Indian dish that is a staple of Punjabi cuisine and a popular "
            "street food across Delhi and beyond. It consists of spicy, tangy chickpea curry (chole) paired "
            "with deep-fried fluffy bread (bhature). The chole is slow-cooked with a rich blend of whole spices, "
            "onion-tomato masala and dried pomegranate seeds giving it a distinctive dark colour and bold flavour. "
            "It is a celebratory dish often eaten on weekends and special occasions."
        ),
        'ingredients': [
            'Chickpeas (kabuli chana)', 'Onions', 'Tomatoes', 'Ginger-garlic paste',
            'Chole masala', 'Anardana (dried pomegranate seeds)', 'Bay leaves', 'Black cardamom',
            'Maida (refined flour) for bhature', 'Curd', 'Baking soda', 'Oil for frying'
        ],
        'preparation': (
            "1. Soak chickpeas overnight and pressure cook until tender. "
            "2. Prepare masala by sauteing onions, ginger-garlic paste and tomatoes with whole spices and chole masala; add chickpeas and simmer for 20 minutes. "
            "3. For bhature, knead maida with curd, a pinch of baking soda and salt into a soft dough; rest for 2 hours. "
            "4. Roll into oval shapes and deep fry in hot oil until puffed and golden."
        ),
        'serving_suggestions': (
            "Serve the hot bhature alongside a generous bowl of chole, garnished with sliced onions, "
            "green chilli, lemon wedge and a side of pickled carrots and radish (gajar mooli ka achar)."
        ),
        'origin': 'Delhi & Punjab, India',
        'history': (
            "Chole Bhature is believed to have originated in the Punjabi dhabas of Delhi in the early 20th century. "
            "It became a defining dish of Delhi street food culture and spread rapidly across North India. "
            "Today it is served everywhere from roadside stalls to upscale restaurants and is a beloved weekend breakfast tradition."
        ),
        'famous_for': {
            'city': 'Delhi',
            'text': (
                "Chole Bhature is the pride of {city}'s street food scene, where it has been a weekend breakfast "
                "ritual for generations. It is famous for its fiery, tangy chickpea curry paired with pillowy "
                "deep-fried bhature — a combination that is bold, indulgent and utterly unforgettable."
            ),
        },
    },
    'Dhokla': {
        'long_description': (
            "Dhokla is a light, spongy and nutritious steamed snack originating from the state of Gujarat. "
            "Made from a fermented batter of gram flour (besan) and curd, it is steamed to a soft, airy texture "
            "and then tempered with a fragrant tadka of mustard seeds, curry leaves and green chillies. "
            "It is naturally low in fat, high in protein and completely vegan, making it one of the healthiest "
            "Indian snacks. It is enjoyed across India as a breakfast, snack or even a light meal."
        ),
        'ingredients': [
            'Gram flour (besan)', 'Curd (yogurt)', 'Ginger-green chilli paste',
            'Turmeric powder', 'Eno fruit salt / baking soda', 'Sugar', 'Salt',
            'Mustard seeds', 'Curry leaves', 'Green chillies', 'Oil', 'Fresh coriander', 'Grated coconut'
        ],
        'preparation': (
            "1. Mix besan, curd, ginger-chilli paste, turmeric, sugar and salt into a smooth batter; rest for 30 minutes. "
            "2. Just before steaming, add Eno fruit salt and mix gently to create a fluffy batter. "
            "3. Pour into a greased plate and steam for 15-18 minutes until a toothpick comes out clean. "
            "4. Prepare tadka by heating oil, adding mustard seeds, curry leaves and green chillies; pour over the dhokla and cut into squares."
        ),
        'serving_suggestions': (
            "Serve warm with green mint-coriander chutney and sweet tamarind chutney on the side. "
            "Garnish with fresh coriander and grated coconut for extra flavour and visual appeal."
        ),
        'origin': 'Gujarat, India',
        'history': (
            "Dhokla has been a part of Gujarati cuisine for over 500 years and is mentioned in ancient texts "
            "dating back to 1066 AD. It originated as a home-cooked snack in Gujarat and gradually spread "
            "across India, becoming one of the most recognised symbols of Gujarati food culture worldwide."
        ),
        'famous_for': {
            'city': 'Gujarat',
            'text': (
                "Dhokla is the most iconic snack from {city}, celebrated across India for its light, spongy "
                "texture and tangy-sweet flavour. It is famous for being one of the healthiest Indian snacks — "
                "steamed, oil-free and packed with protein — making it a guilt-free favourite at any time of day."
            ),
        },
    },
    'Dosa': {
        'long_description': (
            "Dosa is a thin, crispy crepe made from a fermented batter of rice and urad dal (black lentils), "
            "and is one of the most iconic dishes of South Indian cuisine. It is a staple breakfast across "
            "Tamil Nadu, Karnataka, Andhra Pradesh and Kerala, and has gained popularity worldwide. "
            "The fermentation process gives dosa its characteristic slight tanginess and makes it highly digestible. "
            "It can be plain (sada dosa) or stuffed with spiced potato filling (masala dosa)."
        ),
        'ingredients': [
            'Parboiled rice', 'Urad dal (black lentils)', 'Fenugreek seeds (methi)',
            'Salt', 'Oil / ghee for cooking',
            'For masala filling: boiled potatoes, onions, mustard seeds, curry leaves, turmeric, green chillies'
        ],
        'preparation': (
            "1. Soak rice and urad dal separately for 6-8 hours; grind to a smooth batter and ferment overnight. "
            "2. Add salt to the batter and mix well. "
            "3. Heat a flat iron tawa, pour a ladle of batter and spread in a circular motion to a thin crepe. "
            "4. Drizzle oil around the edges and cook until the base is golden and crispy; fold and serve."
        ),
        'serving_suggestions': (
            "Serve hot with coconut chutney, tomato chutney and a bowl of hot sambar. "
            "For masala dosa, place the potato filling in the centre before folding."
        ),
        'origin': 'Udupi, Karnataka, India',
        'history': (
            "Dosa is believed to have originated in the Udupi region of Karnataka over 1,000 years ago, "
            "with references found in Tamil Sangam literature. It spread across South India through Udupi "
            "restaurants and became a global ambassador of Indian cuisine, now enjoyed in over 100 countries."
        ),
        'famous_for': {
            'city': 'Udupi',
            'text': (
                "Dosa originated in {city}, Karnataka, and became the most iconic breakfast of South India. "
                "It is famous for its paper-thin crispy texture, subtle fermented tang and incredible versatility — "
                "from the classic plain dosa to the indulgent masala dosa stuffed with spiced potatoes."
            ),
        },
    },
    'Grilled Sandwich': {
        'long_description': (
            "The Mumbai-style grilled sandwich is a popular street food and quick breakfast option found at "
            "every corner of the city. Thick slices of white bread are layered with butter, mint chutney, "
            "boiled potato slices, tomato, cucumber, onion and cheese, then pressed in a sandwich griller "
            "until golden and crispy. The combination of the cool chutney, fresh vegetables and melted cheese "
            "inside a crunchy toasted exterior makes it an irresistible snack at any time of day."
        ),
        'ingredients': [
            'White bread slices', 'Butter', 'Mint-coriander chutney', 'Boiled potato (sliced)',
            'Tomato slices', 'Cucumber slices', 'Onion slices', 'Cheese (processed / cheddar)',
            'Chaat masala', 'Salt & pepper'
        ],
        'preparation': (
            "1. Spread butter generously on all bread slices, then apply mint chutney on one side. "
            "2. Layer boiled potato, tomato, cucumber and onion slices; sprinkle chaat masala and salt. "
            "3. Place cheese on top and close the sandwich. "
            "4. Grill in a sandwich press for 3-4 minutes until golden brown and cheese is melted."
        ),
        'serving_suggestions': (
            "Cut diagonally and serve hot with extra mint chutney and tomato ketchup. "
            "A cup of masala chai on the side makes it the perfect Mumbai breakfast."
        ),
        'origin': 'Mumbai, India',
        'history': (
            "The grilled sandwich became a Mumbai street food icon in the 1970s, popularised by the city's "
            "countless sandwich stalls outside railway stations and offices. The addition of mint chutney "
            "and chaat masala gave it a uniquely Indian character, and it remains one of Mumbai's most "
            "affordable and beloved quick meals."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "The grilled sandwich is a beloved street food staple of {city}, found at every railway "
                "station stall and office-side cart. It is famous for the irresistible combination of "
                "cool mint chutney, fresh vegetables and melted cheese pressed inside a golden, crispy toasted bread."
            ),
        },
    },
    'Idli': {
        'long_description': (
            "Idli is a soft, fluffy steamed rice cake that is one of the oldest and most nutritious breakfast "
            "foods in South India. Made from a fermented batter of rice and urad dal, idlis are steamed in "
            "special moulds to produce their characteristic round, pillow-soft shape. They are completely "
            "oil-free, low in calories and easy to digest, making them ideal for all age groups. "
            "Idli is a cornerstone of South Indian cuisine and is enjoyed daily in millions of households."
        ),
        'ingredients': [
            'Idli rice (parboiled rice)', 'Urad dal (black lentils)', 'Fenugreek seeds',
            'Salt', 'Water'
        ],
        'preparation': (
            "1. Soak idli rice and urad dal separately for 6-8 hours. "
            "2. Grind urad dal to a smooth, fluffy batter and rice to a slightly coarse batter; mix together with salt. "
            "3. Ferment the batter in a warm place for 8-12 hours until it doubles in volume. "
            "4. Pour batter into greased idli moulds and steam for 10-12 minutes until a skewer comes out clean."
        ),
        'serving_suggestions': (
            "Serve hot with coconut chutney, tomato-onion chutney and a bowl of piping hot sambar. "
            "A drizzle of ghee on top of the idlis adds richness and enhances the flavour."
        ),
        'origin': 'South India (Tamil Nadu / Karnataka)',
        'history': (
            "Idli is one of the oldest foods in Indian culinary history, with references dating back to "
            "920 AD in Kannada literature. It is believed to have evolved from Indonesian steamed rice cakes "
            "brought to South India by traders. Today it is the most consumed breakfast dish in South India "
            "and a staple in millions of homes daily."
        ),
        'famous_for': {
            'city': 'Tamil Nadu',
            'text': (
                "Idli is the quintessential breakfast of {city} and all of South India, eaten daily by millions. "
                "It is famous for being completely oil-free, light on the stomach and deeply nourishing — "
                "a perfect start to the day when paired with coconut chutney and hot sambar."
            ),
        },
    },
    'Medu Vada': {
        'long_description': (
            "Medu Vada is a crispy, golden-fried savoury doughnut from South India, made from a thick batter "
            "of urad dal. The name 'medu' means soft in Kannada, referring to the fluffy interior that contrasts "
            "beautifully with the crunchy exterior. It is a staple breakfast and snack across Karnataka, Tamil Nadu "
            "and Kerala. The characteristic hole in the centre ensures even cooking. It is rich in protein from "
            "the lentils and is a beloved comfort food enjoyed with sambar and chutney."
        ),
        'ingredients': [
            'Urad dal (black lentils)', 'Green chillies', 'Ginger', 'Curry leaves',
            'Black pepper', 'Cumin seeds', 'Salt', 'Oil for deep frying'
        ],
        'preparation': (
            "1. Soak urad dal for 4-6 hours; drain and grind to a thick, fluffy batter using minimal water. "
            "2. Add chopped green chillies, ginger, curry leaves, pepper, cumin and salt; mix well. "
            "3. Wet your hands, take a portion of batter, shape into a ball, make a hole in the centre with your thumb. "
            "4. Slide gently into hot oil and deep fry on medium heat until golden and crispy on both sides."
        ),
        'serving_suggestions': (
            "Serve immediately while hot and crispy with coconut chutney and a bowl of hot sambar for dipping. "
            "Also delicious when soaked in sambar as 'sambar vada'."
        ),
        'origin': 'Karnataka, India',
        'history': (
            "Medu Vada has been a part of South Indian cuisine for over a thousand years and is mentioned "
            "in ancient Kannada texts. It originated in the temple kitchens of Karnataka as a prasad offering "
            "and gradually became a popular everyday breakfast and snack across Tamil Nadu, Kerala and Andhra Pradesh."
        ),
        'famous_for': {
            'city': 'Karnataka',
            'text': (
                "Medu Vada is a breakfast icon from {city} and the wider South Indian region. "
                "It is famous for its addictive contrast of a shatteringly crispy golden exterior and a "
                "soft, fluffy lentil interior — best enjoyed dunked into hot sambar or paired with coconut chutney."
            ),
        },
    },
    'Misal Pav': {
        'long_description': (
            "Misal Pav is a fiery, flavour-packed street food from Maharashtra, particularly famous in Pune and Nashik. "
            "It consists of a spicy sprouted moth bean (matki) curry topped with a crunchy mixture of farsan (fried snacks), "
            "chopped onions, tomatoes and fresh coriander, served with soft pav (bread rolls). "
            "The dish has multiple regional variations - Kolhapuri misal is the spiciest, while Puneri misal is milder. "
            "It is a complete meal packed with protein from the sprouts and carbohydrates from the pav."
        ),
        'ingredients': [
            'Sprouted moth beans (matki)', 'Onions', 'Tomatoes', 'Ginger-garlic paste',
            'Misal masala / goda masala', 'Coconut (grated)', 'Farsan / chivda (fried snack mix)',
            'Pav (bread rolls)', 'Fresh coriander', 'Lemon', 'Oil'
        ],
        'preparation': (
            "1. Pressure cook sprouted matki with turmeric and salt until just tender. "
            "2. Prepare a spicy gravy (kat) by sauteing onions, tomatoes, ginger-garlic paste with misal masala and coconut; add water and simmer. "
            "3. Add cooked sprouts to the gravy and cook for 10 minutes. "
            "4. Serve in a bowl topped with farsan, chopped onion, tomato, coriander and a squeeze of lemon alongside toasted pav."
        ),
        'serving_suggestions': (
            "Serve with buttered and toasted pav, a wedge of lemon and extra farsan on the side. "
            "Accompany with a small bowl of plain curd to balance the heat."
        ),
        'origin': 'Pune & Nashik, Maharashtra, India',
        'history': (
            "Misal Pav is believed to have originated in the Pune and Nashik regions of Maharashtra in the "
            "early 20th century as a protein-rich, affordable meal for working-class communities. "
            "Each region developed its own variation — Kolhapuri misal is fiery red, while Puneri misal is "
            "milder — and the dish is now considered the unofficial breakfast of Maharashtra."
        ),
        'famous_for': {
            'city': 'Pune',
            'text': (
                "Misal Pav is the unofficial breakfast king of {city} and all of Maharashtra. "
                "It is famous for its explosive spice, the satisfying crunch of farsan on top of a rich "
                "sprouted lentil curry, and the way a simple buttered pav perfectly balances all that heat."
            ),
        },
    },
    'Momos': {
        'long_description': (
            "Momos are steamed or fried dumplings that originated in Tibet and Nepal and have become one of "
            "the most popular street foods across North India, especially in Delhi, Darjeeling and the Northeast. "
            "A thin dough wrapper is filled with a spiced mixture of vegetables (or meat), then pleated and "
            "steamed or fried to perfection. They are served with a fiery red chilli chutney that is as iconic "
            "as the momos themselves. Their soft, juicy filling and delicate wrapper make them utterly addictive."
        ),
        'ingredients': [
            'Maida (all-purpose flour)', 'Cabbage (finely chopped)', 'Carrots (grated)',
            'Onions', 'Garlic', 'Ginger', 'Soy sauce', 'Black pepper',
            'Salt', 'Oil', 'Spring onions'
        ],
        'preparation': (
            "1. Knead maida with water and a pinch of salt into a stiff dough; rest for 30 minutes. "
            "2. Saute finely chopped vegetables with garlic, ginger, soy sauce, pepper and salt until cooked; cool completely. "
            "3. Roll dough into thin circles, place filling in the centre and pleat the edges to seal. "
            "4. Steam in a steamer for 10-12 minutes until the wrapper turns slightly translucent."
        ),
        'serving_suggestions': (
            "Serve hot with spicy red chilli-garlic chutney and a clear soup (thukpa) on the side. "
            "Pan-fried or tandoori momos are popular variations for extra texture."
        ),
        'origin': 'Tibet / Nepal (popularised in Delhi, India)',
        'history': (
            "Momos originated in Tibet and Nepal, where they have been a staple food for centuries. "
            "They were introduced to India by Tibetan refugees who settled in Delhi and Darjeeling in the "
            "1960s. Over the following decades they spread across North India and became one of the most "
            "popular street foods in Delhi, with hundreds of momo stalls operating in every neighbourhood."
        ),
        'famous_for': {
            'city': 'Delhi',
            'text': (
                "Momos became a street food phenomenon in {city}, where they are sold at thousands of stalls "
                "across every neighbourhood. They are famous for their juicy, spiced vegetable filling wrapped "
                "in a delicate steamed dough, served with a fiery red chutney that is as iconic as the momos themselves."
            ),
        },
    },
    'Pakoda': {
        'long_description': (
            "Pakoda (also called pakora or bhajiya) is India's ultimate monsoon snack - crispy, golden fritters "
            "made by dipping vegetables in a spiced gram flour batter and deep frying them. From onion pakodas "
            "to spinach, paneer, potato and chilli pakodas, the variety is endless. They are found at every "
            "tea stall and street corner across India and are inseparable from a hot cup of masala chai on a "
            "rainy day. Simple to make yet deeply satisfying, pakodas are a true comfort food."
        ),
        'ingredients': [
            'Gram flour (besan)', 'Onions / potatoes / spinach / paneer (choice of vegetable)',
            'Green chillies', 'Ginger', 'Turmeric', 'Red chilli powder', 'Ajwain (carom seeds)',
            'Coriander leaves', 'Salt', 'Oil for deep frying'
        ],
        'preparation': (
            "1. Make a thick batter by mixing besan with turmeric, red chilli powder, ajwain, salt and water. "
            "2. Slice vegetables thinly and mix into the batter, or dip individual pieces to coat. "
            "3. Heat oil in a deep pan; drop spoonfuls of batter-coated vegetables into hot oil. "
            "4. Fry on medium heat, turning occasionally, until golden and crispy; drain on paper towels."
        ),
        'serving_suggestions': (
            "Serve piping hot with green mint chutney and tamarind chutney. "
            "Best enjoyed with a hot cup of masala chai on a rainy or cold day."
        ),
        'origin': 'Pan India',
        'history': (
            "Pakoda has been a part of Indian cuisine for centuries, with references in ancient Sanskrit "
            "texts describing fried gram flour fritters. It became a ubiquitous street food across the "
            "entire subcontinent and is deeply associated with the monsoon season. Every region has its "
            "own variation — from onion bhajiya in Maharashtra to mirchi pakoda in Rajasthan."
        ),
        'famous_for': {
            'city': 'India',
            'text': (
                "Pakoda is loved across all of {city} as the ultimate monsoon comfort food. "
                "It is famous for its irresistibly crispy gram flour coating, the endless variety of fillings, "
                "and its inseparable bond with a hot cup of masala chai on a rainy afternoon."
            ),
        },
    },
    'Pani Puri': {
        'long_description': (
            "Pani Puri - known as Golgappa in Delhi and Puchka in Kolkata - is arguably India's most beloved "
            "street food. It consists of hollow, crispy fried puris filled with a mixture of spiced mashed "
            "potatoes, chickpeas and tangy tamarind chutney, then dunked into ice-cold spiced mint water (pani) "
            "and eaten in one bite. The explosion of flavours - spicy, tangy, sweet and savoury all at once - "
            "makes it an unmatched sensory experience. It is enjoyed by millions across India every single day."
        ),
        'ingredients': [
            'Semolina (sooji) or maida for puris', 'Boiled potatoes', 'Boiled chickpeas',
            'Tamarind chutney', 'Mint leaves', 'Coriander leaves', 'Green chillies',
            'Black salt (kala namak)', 'Roasted cumin powder', 'Chaat masala', 'Water', 'Oil for frying'
        ],
        'preparation': (
            "1. Knead semolina into a stiff dough, roll thin and cut into small circles; deep fry until puffed and crispy. "
            "2. Blend mint, coriander, green chillies, black salt, cumin powder and chaat masala with cold water to make the pani. "
            "3. Prepare filling by mashing boiled potatoes with chickpeas, chaat masala and tamarind chutney. "
            "4. Make a small hole in each puri, fill with potato mixture, dip in pani and serve immediately."
        ),
        'serving_suggestions': (
            "Serve immediately after filling - they go soggy quickly. "
            "Offer both spicy green pani and sweet tamarind pani so guests can choose their preference."
        ),
        'origin': 'Magadha (Bihar), India',
        'history': (
            "Pani Puri is believed to have originated in the Magadha region of present-day Bihar, with "
            "legends linking it to the Mahabharata era. It spread across India under different names — "
            "Golgappa in Delhi, Puchka in Kolkata, and Pani Puri in Mumbai — and is today considered "
            "the most widely eaten street food in the entire country."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "Pani Puri is famous across India but reaches its most beloved form on the streets of {city}. "
                "It is celebrated for the explosive burst of flavour in every single bite — spicy, tangy, "
                "sweet and sour all at once — making it the most addictive and universally loved Indian street food."
            ),
        },
    },
    'Pav Bhaji': {
        'long_description': (
            "Pav Bhaji is a quintessential Mumbai street food that was originally created as a quick, filling "
            "meal for textile mill workers in the 1850s. It is a thick, spiced mash of mixed vegetables - "
            "potatoes, peas, cauliflower, capsicum and tomatoes - cooked on a large flat tawa with generous "
            "amounts of butter and a special pav bhaji masala. It is served with soft, buttered and toasted "
            "pav (bread rolls). Today it is enjoyed across India and is a staple at street stalls and restaurants alike."
        ),
        'ingredients': [
            'Potatoes', 'Cauliflower', 'Green peas', 'Capsicum', 'Tomatoes', 'Onions',
            'Pav bhaji masala', 'Butter', 'Ginger-garlic paste', 'Red chilli powder',
            'Turmeric', 'Pav (bread rolls)', 'Lemon', 'Fresh coriander'
        ],
        'preparation': (
            "1. Boil and mash potatoes, cauliflower and peas together. "
            "2. On a hot tawa, melt butter and saute onions, capsicum and tomatoes with ginger-garlic paste. "
            "3. Add mashed vegetables, pav bhaji masala, red chilli powder and salt; mash everything together and cook for 15 minutes, adding water as needed. "
            "4. Slice pav, apply butter and toast on the tawa until golden; serve alongside the bhaji."
        ),
        'serving_suggestions': (
            "Serve bhaji topped with a cube of butter, chopped onions, coriander and a lemon wedge. "
            "Accompany with 2 toasted buttered pavs. A side of finely chopped raw onion with lemon is traditional."
        ),
        'origin': 'Mumbai, India',
        'history': (
            "Pav Bhaji was invented in Mumbai in the 1850s as a quick, nutritious meal for textile mill "
            "workers who needed a fast lunch during short breaks. Street vendor Tiba Bhatt is often credited "
            "with creating the dish by mashing leftover vegetables together on a tawa. It became a Mumbai "
            "institution and is now one of the most popular street foods across India."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "Pav Bhaji is one of the most iconic street foods of {city}, born on the city's bustling "
                "tawa-sizzling street corners. It is famous for its rich, buttery spiced vegetable mash "
                "and the way a perfectly toasted, butter-soaked pav makes every bite deeply satisfying."
            ),
        },
    },
    'Poha': {
        'long_description': (
            "Poha is a light, quick and nutritious breakfast dish made from flattened rice (beaten rice) and "
            "is especially popular in Madhya Pradesh, Maharashtra and Gujarat. The flattened rice is rinsed, "
            "drained and tossed in a tempering of mustard seeds, curry leaves, onions, green chillies and "
            "turmeric, then garnished with fresh coriander, lemon juice and sev. It is ready in under 15 minutes, "
            "making it one of the most practical and wholesome morning meals in Indian cuisine."
        ),
        'ingredients': [
            'Flattened rice (poha / chivda)', 'Onions', 'Green chillies', 'Mustard seeds',
            'Curry leaves', 'Turmeric powder', 'Roasted peanuts', 'Sugar', 'Salt',
            'Lemon juice', 'Fresh coriander', 'Sev (for garnish)', 'Oil'
        ],
        'preparation': (
            "1. Rinse poha in water, drain and let it soften for 5 minutes; sprinkle salt and turmeric and mix gently. "
            "2. Heat oil in a pan, add mustard seeds; once they splutter add curry leaves, green chillies and onions; saute until translucent. "
            "3. Add roasted peanuts and the seasoned poha; mix gently and cook for 3-4 minutes on low heat. "
            "4. Finish with a squeeze of lemon juice and garnish with fresh coriander and sev."
        ),
        'serving_suggestions': (
            "Serve warm garnished with sev, fresh coriander and a wedge of lemon. "
            "Pairs perfectly with a hot cup of masala chai or filter coffee."
        ),
        'origin': 'Madhya Pradesh & Maharashtra, India',
        'history': (
            "Poha has been a staple breakfast in central India for centuries, particularly in Madhya Pradesh "
            "and Maharashtra. The city of Indore is especially famous for its unique style of poha served "
            "with jalebi. It is one of the simplest and most nutritious Indian breakfasts and is now popular "
            "across the country as a light, quick morning meal."
        ),
        'famous_for': {
            'city': 'Indore',
            'text': (
                "Poha is most famously associated with {city} in Madhya Pradesh, where it is served with "
                "crispy sev and a side of jalebi in a combination that has become legendary. "
                "It is loved across India for being a light, quick and wholesome breakfast that comes together in under 15 minutes."
            ),
        },
    },
    'Samosa': {
        'long_description': (
            "Samosa is perhaps the most universally recognised Indian snack - a crispy, triangular pastry "
            "filled with a spiced potato and pea mixture, deep fried to a golden perfection. It has been a "
            "part of Indian street food culture for centuries and is found everywhere from roadside stalls to "
            "five-star hotel menus. The outer shell is made from maida and is characteristically flaky and "
            "crunchy, while the filling is warmly spiced with cumin, coriander and amchur. No Indian tea-time "
            "is complete without a samosa."
        ),
        'ingredients': [
            'Maida (all-purpose flour)', 'Ajwain (carom seeds)', 'Oil (for dough and frying)',
            'Boiled potatoes', 'Green peas', 'Cumin seeds', 'Coriander powder',
            'Garam masala', 'Amchur (dry mango powder)', 'Green chillies', 'Ginger', 'Salt'
        ],
        'preparation': (
            "1. Make a stiff dough with maida, ajwain, oil and salt; rest for 30 minutes. "
            "2. Prepare filling: saute cumin, ginger and green chillies, add boiled potatoes and peas with all spices; cool completely. "
            "3. Roll dough into ovals, cut in half, form a cone, fill with potato mixture and seal edges with water. "
            "4. Deep fry on medium-low heat for 8-10 minutes until evenly golden and crispy."
        ),
        'serving_suggestions': (
            "Serve hot with green mint-coriander chutney and sweet tamarind chutney. "
            "A popular variation is 'samosa chaat' - crushed samosa topped with chutneys, curd and sev."
        ),
        'origin': 'Central Asia (popularised across India)',
        'history': (
            "The samosa originated in Central Asia and the Middle East, where it was known as 'sambosa', "
            "and was brought to India by traders and merchants during the 13th and 14th centuries. "
            "It was quickly adopted and adapted by Indian cooks, who filled it with spiced potatoes and peas. "
            "Today it is one of the most iconic and universally loved snacks across the entire Indian subcontinent."
        ),
        'famous_for': {
            'city': 'North India',
            'text': (
                "Samosa is the most universally recognised Indian snack, especially beloved across {city}. "
                "It is famous for its perfectly crispy, flaky pastry shell encasing a warmly spiced potato "
                "and pea filling — a timeless combination that has made it a staple at every tea stall, "
                "railway platform and festive gathering across the country."
            ),
        },
    },
    'Sev Puri': {
        'long_description': (
            "Sev Puri is a popular Mumbai chaat that is as vibrant in appearance as it is in flavour. "
            "Small, crispy flat puris are topped with diced boiled potatoes, chopped onions and tomatoes, "
            "then drizzled with green chutney and sweet tamarind chutney, and finally buried under a generous "
            "heap of thin, crispy sev. Every bite delivers a perfect balance of crunch, tang, sweetness and spice. "
            "It is a favourite at chaat stalls across Maharashtra and is best eaten immediately before the puris lose their crunch."
        ),
        'ingredients': [
            'Flat crispy puris', 'Boiled potatoes (diced)', 'Onions (finely chopped)',
            'Tomatoes (finely chopped)', 'Thin sev', 'Green mint-coriander chutney',
            'Sweet tamarind chutney', 'Chaat masala', 'Red chilli powder', 'Fresh coriander'
        ],
        'preparation': (
            "1. Arrange flat puris on a plate. "
            "2. Place a small amount of diced boiled potato on each puri. "
            "3. Top with chopped onions and tomatoes; drizzle green chutney and tamarind chutney generously. "
            "4. Sprinkle chaat masala and red chilli powder, then cover with a thick layer of sev and garnish with coriander."
        ),
        'serving_suggestions': (
            "Serve immediately - sev puri must be eaten right away to enjoy the contrast of crispy puri and soft toppings. "
            "Best enjoyed as an evening snack with a cup of masala chai."
        ),
        'origin': 'Mumbai, Maharashtra, India',
        'history': (
            "Sev Puri is a creation of Mumbai's vibrant chaat culture, believed to have been developed by "
            "chaat vendors in the city during the mid-20th century. It is a variation of the older papdi chaat "
            "tradition and became a signature Mumbai street food. Today it is a staple at chaat stalls across "
            "Maharashtra and has spread to cities throughout India."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "Sev Puri is a signature chaat of {city}, born from the city's vibrant street food culture. "
                "It is famous for the perfect harmony of textures and flavours — crispy puri, soft potato, "
                "crunchy sev, tangy tamarind and spicy green chutney — all in one irresistible bite."
            ),
        },
    },
    'Vada Pav': {
        'long_description': (
            "Vada Pav is Mumbai's most iconic street food and is often called the 'Indian Burger'. "
            "A spiced, deep-fried potato fritter (vada) is sandwiched inside a soft bread roll (pav) "
            "along with dry garlic chutney, green chutney and fried green chilli. It was invented in Mumbai "
            "in the 1960s and quickly became the go-to affordable meal for the city's working class. "
            "Today it is a cultural symbol of Mumbai and is eaten by people from all walks of life, "
            "from street corners to office canteens."
        ),
        'ingredients': [
            'Pav (bread rolls)', 'Boiled potatoes', 'Mustard seeds', 'Curry leaves',
            'Turmeric', 'Green chillies', 'Ginger-garlic paste', 'Gram flour (besan)',
            'Dry garlic chutney (lehsun chutney)', 'Green mint chutney', 'Oil for frying'
        ],
        'preparation': (
            "1. Prepare vada filling: temper mustard seeds and curry leaves in oil, add ginger-garlic paste, green chillies and mashed potatoes with turmeric; shape into balls. "
            "2. Make a thin batter with besan, turmeric and salt; dip potato balls and deep fry until golden. "
            "3. Prepare dry garlic chutney by grinding roasted garlic, dried coconut, red chilli and salt. "
            "4. Slice pav, spread green chutney on one side and dry garlic chutney on the other; place hot vada inside and serve."
        ),
        'serving_suggestions': (
            "Serve immediately with a fried green chilli on the side and extra dry garlic chutney. "
            "A cup of hot cutting chai is the traditional accompaniment on Mumbai streets."
        ),
        'origin': 'Mumbai, Maharashtra, India',
        'history': (
            "Vada Pav was invented in 1966 by Ashok Vaidya, a street vendor outside Dadar railway station "
            "in Mumbai. It was created as an affordable, filling meal for the city's mill workers and commuters. "
            "It quickly became Mumbai's most iconic street food and is now sold at over 40,000 stalls across "
            "the city, earning it the title of Mumbai's unofficial official food."
        ),
        'famous_for': {
            'city': 'Mumbai',
            'text': (
                "Vada Pav is the soul of {city}'s street food culture and is often called the 'Indian Burger'. "
                "It is famous for its spiced, crispy potato vada nestled in a soft pav with fiery dry garlic "
                "chutney — a combination so perfect that it has fed the city's millions for over five decades."
            ),
        },
    },
}
# -- UI ------------------------------------------------------------------------
st.title("Food Recognition & Nutrition Analysis")

all_foods = db.get_all_foods()
food_name_map = {}
for f in all_foods:
    food_name_map[f['name'].strip()] = f
    food_name_map[f['name'].strip().lower()] = f

def lookup_food(name):
    return food_name_map.get(name.strip()) or food_name_map.get(name.strip().lower())

if model:
    st.success("AI Model loaded! Real predictions active.")
else:
    st.warning("No trained model found. Run `python train_model.py` to train the model first.")

st.info("Upload an image of Indian street food to get instant recognition and nutrition info!")

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Uploaded Image")
        st.image(image, width=400)

        st.subheader("Portion Size")
        portion = st.select_slider(
            "Select portion size:",
            options=["Small", "Medium", "Large", "Extra Large"],
            value="Medium"
        )
        portion_multipliers = {"Small": 0.7, "Medium": 1.0, "Large": 1.3, "Extra Large": 1.6}
        portion_descriptions = {
            "Small":       ("", "A light bite - about 70% of a standard serving. Great for snacking or watching your intake."),
            "Medium":      ("", "A standard serving - just the right amount for a satisfying meal without overdoing it."),
            "Large":       ("", "A generous helping - 30% more than usual. Perfect when you're really hungry."),
            "Extra Large": ("", "A hearty feast - 60% more than a standard serving. Go all in!")
        }
        multiplier = portion_multipliers[portion]
        icon, desc = portion_descriptions[portion]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e3a5f,#0f2540);border-left:4px solid #4fc3f7;
                    border-radius:10px;padding:14px 18px;margin-top:8px;color:#e0f7fa;font-size:0.92rem;line-height:1.6;">
            <span style="font-size:1.4rem">{icon}</span>
            <strong style="color:#4fc3f7;font-size:1rem;"> {portion} Portion</strong><br>
            <span style="color:#b0bec5;">{desc}</span>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("Prediction Results")
        with st.spinner("Analyzing image..."):
            import time
            time.sleep(0.5)
            predicted_food, confidence, used_model = predict_food(image)

            hour = datetime.now().hour
            if 5 <= hour < 11:
                meal_type = "Breakfast"
            elif 11 <= hour < 16:
                meal_type = "Lunch"
            elif 16 <= hour < 22:
                meal_type = "Dinner"
            else:
                meal_type = "Snack"

            if not used_model:
                st.error("No trained model found. Please train the model first by running `python train_model.py`.")
                st.stop()

            if predicted_food == 'Unknown':
                st.error("This image is not a recognized Indian street food!")
                st.warning(f"Confidence was too low ({confidence*100:.1f}%) or the food is not in our database.")
                st.info("Please upload a clear image of one of the supported Indian street food items.")
                st.stop()

            st.success(f"Detected: {predicted_food}")
            col_a, col_b = st.columns(2)
            col_a.metric("Confidence", f"{confidence*100:.1f}%")
            col_b.metric("Meal Type", meal_type)

            food = lookup_food(predicted_food)

            if food:
                st.divider()
                st.subheader("Nutrition Information")
                st.caption(f"Per serving: {food['serving_size']} ({portion} portion)")
                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("Calories", f"{int(food['calories'] * multiplier)} kcal")
                col_b.metric("Protein", f"{food['protein'] * multiplier:.1f}g")
                col_c.metric("Carbs", f"{food['carbohydrates'] * multiplier:.1f}g")
                col_d.metric("Fats", f"{food['fats'] * multiplier:.1f}g")

                st.divider()
                st.subheader("Health Insights")
                calories = food['calories'] * multiplier
                if calories > 400:
                    st.warning(f"High calorie content ({int(calories)} kcal)")
                else:
                    st.success(f"Moderate calorie content ({int(calories)} kcal)")

                allergens = json.loads(food['allergens']) if food['allergens'] else []
                if allergens:
                    st.error(f"Allergen Alert: Contains {', '.join(allergens)}")

                # dietary cards rendered full-width below columns

            else:
                st.warning(f"Nutrition data for '{predicted_food}' not found in database.")
                st.info("Run `python database/seed_data.py` to populate nutrition data.")

    # ── Full-width section below columns ──────────────────────────────────────
    if 'food' in dir() and food and 'predicted_food' in dir() and predicted_food and predicted_food != 'Unknown':
        region_map = {
            'north': 'North India', 'south': 'South India',
            'mumbai': 'Mumbai / Maharashtra', 'maharashtra': 'Maharashtra',
            'gujarat': 'Gujarat', 'central': 'Central India', 'all': 'Pan India'
        }
        region_label   = region_map.get(food.get('region', '').lower(), food.get('region', 'N/A').title())
        meal_types     = food.get('meal_type', '').replace(',', ' · ').title()
        category_label = food.get('category', 'N/A').replace('_', ' ').title()

        st.divider()
        # Quick info badges
        st.markdown(f"""
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;">
            <span style="background:#1e3a5f;color:#4fc3f7;padding:5px 14px;border-radius:20px;font-size:0.85rem;">📍 {region_label}</span>
            <span style="background:#1e3a5f;color:#81c784;padding:5px 14px;border-radius:20px;font-size:0.85rem;">🍴 {meal_types}</span>
            <span style="background:#1e3a5f;color:#ffb74d;padding:5px 14px;border-radius:20px;font-size:0.85rem;">🏷️ {category_label}</span>
            <span style="background:#1e3a5f;color:#f48fb1;padding:5px 14px;border-radius:20px;font-size:0.85rem;">⚖️ {food['serving_size']} ({food.get('serving_size_grams','N/A')}g)</span>
        </div>""", unsafe_allow_html=True)

        # ── Full-width Dietary Information ────────────────────────────────────
        st.divider()
        st.subheader("🥗 Dietary Information")
        _veg_color    = "#1b5e20" if food['is_vegetarian'] else "#4a0000"
        _veg_border   = "#66bb6a" if food['is_vegetarian'] else "#ef5350"
        _veg_label    = "Vegetarian"    if food['is_vegetarian'] else "Non-Vegetarian"
        _vegan_color  = "#1a3a1a"  if food['is_vegan'] else "#2d2d00"
        _vegan_border = "#a5d6a7"  if food['is_vegan'] else "#fff176"
        _vegan_label  = "Vegan"         if food['is_vegan'] else "Not Vegan"
        _jain_color   = "#3e2723"  if food['is_jain'] else "#1a237e"
        _jain_border  = "#ffcc80"  if food['is_jain'] else "#90caf9"
        _jain_label   = "Jain Friendly" if food['is_jain'] else "Not Jain"
        _spice        = food['spice_level']
        _spice_dots   = "🌶️" * _spice + "⚪" * (5 - _spice)
        _spice_color  = ["#1b3a1b","#2e3a00","#4a2800","#5a1a00","#4a0000"][min(_spice-1,4)] if _spice > 0 else "#1a1a2e"
        _spice_border = ["#81c784","#dce775","#ffb74d","#ff7043","#ef5350"][min(_spice-1,4)] if _spice > 0 else "#90caf9"

        st.markdown(f"""
        <style>
        .diet-card {{
            border-radius: 16px;
            padding: 28px 20px;
            text-align: center;
            border: 2px solid;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: default;
            height: 100%;
        }}
        .diet-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        .diet-icon {{ font-size: 2.4rem; margin-bottom: 10px; }}
        .diet-tag  {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.4px; opacity: 0.75; margin-bottom: 6px; }}
        .diet-val  {{ font-size: 1.05rem; font-weight: 700; }}
        </style>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:10px;margin-bottom:10px;">
            <div class="diet-card" style="background:{_veg_color};border-color:{_veg_border};">
                <div class="diet-icon">🥦</div>
                <div class="diet-tag" style="color:{_veg_border};">Diet Type</div>
                <div class="diet-val" style="color:{_veg_border};">{_veg_label}</div>
            </div>
            <div class="diet-card" style="background:{_vegan_color};border-color:{_vegan_border};">
                <div class="diet-icon">🌱</div>
                <div class="diet-tag" style="color:{_vegan_border};">Vegan</div>
                <div class="diet-val" style="color:{_vegan_border};">{_vegan_label}</div>
            </div>
            <div class="diet-card" style="background:{_jain_color};border-color:{_jain_border};">
                <div class="diet-icon">🪔</div>
                <div class="diet-tag" style="color:{_jain_border};">Jain</div>
                <div class="diet-val" style="color:{_jain_border};">{_jain_label}</div>
            </div>
            <div class="diet-card" style="background:{_spice_color};border-color:{_spice_border};">
                <div class="diet-icon">🌶️</div>
                <div class="diet-tag" style="color:{_spice_border};">Spice Level</div>
                <div class="diet-val" style="color:{_spice_border};">{_spice_dots}&nbsp; {_spice}/5</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        details = FOOD_DETAILS.get(predicted_food)
        if details:

            # ── Famous For ────────────────────────────────────────────────────
            ff = details.get('famous_for')
            if ff:
                city = ff['city']
                ff_text = ff['text'].replace('{city}', f'<span style="background:#1e3a5f;color:#4fc3f7;padding:2px 10px;border-radius:12px;font-weight:700;font-size:0.97rem;">{city}</span>')
                st.divider()
                st.markdown(f"""
                <div style="background:#0f2540;border:2px solid #4fc3f7;border-radius:14px;padding:24px 28px;">
                    <div style="font-size:1.25rem;font-weight:700;color:#4fc3f7;margin-bottom:12px;">⭐ Famous For</div>
                    <div style="color:#cfd8dc;font-size:1rem;line-height:1.9;">{ff_text}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("## 📖 Detailed Food Information")

            # About
            st.markdown("### 📝 About this Dish")
            st.markdown(f"""
            <div style="background:#0f2540;border-left:5px solid #4fc3f7;border-radius:10px;
                        padding:20px 24px;color:#cfd8dc;font-size:1rem;line-height:1.9;margin-bottom:8px;">
                {details['long_description']}
            </div>""", unsafe_allow_html=True)

            st.markdown("")

            # Ingredients + Preparation side by side
            ing_col, prep_col = st.columns([1, 1], gap="large")

            with ing_col:
                st.markdown("### 🧂 Main Ingredients")
                ing_items = "".join(
                    f'<div style="padding:6px 0;border-bottom:1px solid #1e3a5f;color:#cfd8dc;">🔸 {ing}</div>'
                    for ing in details['ingredients']
                )
                st.markdown(f"""
                <div style="background:#0f2540;border-radius:10px;padding:16px 20px;line-height:1.7;">
                    {ing_items}
                </div>""", unsafe_allow_html=True)

            with prep_col:
                st.markdown("### 👨‍🍳 How It Is Prepared")
                steps = details['preparation'].split(". ")
                step_items = "".join(
                    f'<div style="padding:8px 0;border-bottom:1px solid #1e3a5f;color:#cfd8dc;">{s.strip()}{"." if not s.strip().endswith(".") else ""}</div>'
                    for s in steps if s.strip()
                )
                st.markdown(f"""
                <div style="background:#0f2540;border-radius:10px;padding:16px 20px;line-height:1.7;">
                    {step_items}
                </div>""", unsafe_allow_html=True)

            st.markdown("")

            # Serving suggestions
            st.markdown("### 🍽️ Serving Suggestions")
            st.markdown(f"""
            <div style="background:#0f2540;border-left:5px solid #ffb74d;border-radius:10px;
                        padding:20px 24px;color:#cfd8dc;font-size:1rem;line-height:1.9;margin-bottom:8px;">
                🥗 {details['serving_suggestions']}
            </div>""", unsafe_allow_html=True)

            st.markdown("")

            # Food Origin & History
            if details.get('origin') or details.get('history'):
                st.markdown("### 🌍 Food Origin & History")
                st.markdown(f"""
                <div style="background:#0f2540;border:1px solid #1e3a5f;border-radius:12px;
                            padding:24px 28px;margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
                        <span style="font-size:1.6rem;">🗺️</span>
                        <div>
                            <span style="color:#90caf9;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">Origin</span><br>
                            <span style="color:#ffffff;font-size:1.05rem;font-weight:600;">{details.get('origin', 'India')}</span>
                        </div>
                    </div>
                    <div style="border-top:1px solid #1e3a5f;padding-top:14px;color:#cfd8dc;font-size:0.97rem;line-height:1.9;">
                        <span style="color:#90caf9;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">History</span><br>
                        {details.get('history', '')}
                    </div>
                </div>""", unsafe_allow_html=True)

            st.markdown("")

            # Additional nutrition full width
            st.markdown("### 📊 Additional Nutrition")
            n1, n2, n3 = st.columns(3)
            n1.metric("🌾 Fiber",  f"{food.get('fiber',  0) * multiplier:.1f}g")
            n2.metric("🍬 Sugar",  f"{food.get('sugar',  0) * multiplier:.1f}g")
            n3.metric("🧂 Sodium", f"{food.get('sodium', 0) * multiplier:.0f}mg")

        st.divider()
        if st.button("💾 Save to Food Diary", type="primary"):
            user_id = st.session_state.user['id']
            db.save_prediction(
                user_id=user_id,
                food_item_id=food['id'],
                image_path=f"uploads/{user_id}/{uploaded_file.name}",
                predicted_class=predicted_food,
                confidence_score=confidence,
                meal_type=meal_type,
                portion_size=portion,
                portion_multiplier=multiplier
            )
            st.success("Saved to your food diary!")
            st.balloons()

else:
    st.info("Upload an image to get started")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tips for Best Results")
        st.write("- Use clear, well-lit images")
        st.write("- Capture the food from above or at an angle")
        st.write("- Ensure the food is the main focus")
        st.write("- Avoid blurry or dark images")
    with col2:
        st.subheader("Supported Foods")
        for name in CLASS_NAMES[:-1]:
            st.write(f"- {name}")