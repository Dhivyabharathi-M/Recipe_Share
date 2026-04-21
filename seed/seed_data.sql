-- seed_data.sql  –  Sample recipes to populate the database
INSERT INTO recipes (title, ingredients, steps, meal_type, dietary_focus, created_at) VALUES
(
  'Classic Spaghetti Bolognese',
  'pasta, beef, tomato, garlic, olive oil, onion',
  '1. Cook pasta. 2. Sauté onion and garlic. 3. Brown beef. 4. Add tomato and simmer 20 min. 5. Toss with pasta.',
  'Dinner', 'Balanced', datetime('now')
),
(
  'Veggie Omelette',
  'eggs, bell pepper, onion, tomato, olive oil, salt',
  '1. Beat eggs with salt. 2. Sauté vegetables. 3. Pour egg mixture over vegetables. 4. Fold and serve.',
  'Breakfast', 'High Protein', datetime('now')
),
(
  'Chicken Fried Rice',
  'rice, chicken, egg, soy sauce, garlic, green onion',
  '1. Cook rice. 2. Stir-fry chicken. 3. Add rice, egg, soy sauce. 4. Garnish with green onion.',
  'Lunch', 'Balanced', datetime('now')
),
(
  'Avocado Toast',
  'bread, avocado, lemon, salt, pepper, chili flakes',
  '1. Toast bread. 2. Mash avocado with lemon, salt, pepper. 3. Spread on toast. 4. Top with chili flakes.',
  'Breakfast', 'High Carb', datetime('now')
),
(
  'Lentil Soup',
  'lentils, onion, garlic, tomato, cumin, olive oil, salt',
  '1. Sauté onion and garlic. 2. Add lentils, tomato, cumin and water. 3. Simmer 30 min. 4. Season and serve.',
  'Lunch', 'High Protein', datetime('now')
),
(
  'Pesto Pasta',
  'pasta, pine nuts, basil, parmesan, olive oil, garlic',
  '1. Blend basil, pine nuts, parmesan, garlic, olive oil. 2. Cook pasta. 3. Toss with pesto.',
  'Dinner', 'High Carb', datetime('now')
),
(
  'Greek Salad',
  'tomato, cucumber, olive oil, feta, olives, onion, oregano',
  '1. Chop vegetables. 2. Combine with feta and olives. 3. Drizzle olive oil and sprinkle oregano.',
  'Lunch', 'Low Calorie', datetime('now')
),
(
  'Banana Oat Smoothie',
  'oats, banana, milk, honey, cinnamon',
  '1. Blend all ingredients until smooth. 2. Serve chilled.',
  'Breakfast', 'High Carb', datetime('now')
),
(
  'Grilled Salmon',
  'salmon, lemon, garlic, olive oil, salt, pepper, dill',
  '1. Marinate salmon with lemon, garlic, oil. 2. Grill 4 min each side. 3. Garnish with dill.',
  'Dinner', 'High Protein', datetime('now')
),
(
  'Tofu Stir Fry',
  'tofu, broccoli, soy sauce, garlic, sesame oil, ginger',
  '1. Press and cube tofu. 2. Stir-fry tofu until golden. 3. Add broccoli, sauce ingredients. 4. Toss and serve.',
  'Dinner', 'High Protein', datetime('now')
);
