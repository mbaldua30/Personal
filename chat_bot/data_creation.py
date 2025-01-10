import pandas as pd

# Sample car data
car_data = {
    'Toyota': {
        'Corolla': {
            'Sedan': {
                'accessories': ['Floor mats', 'Seat covers', 'Sunshades'],
                'colors': ['Black', 'Beige', 'Gray']
            },
            'SUV': {
                'accessories': ['Roof box', 'Mud guards', 'Seat covers'],
                'colors': ['Red', 'Blue', 'Silver']
            }
        }
    },
    'Honda': {
        'Civic': {
            'Sedan': {
                'accessories': ['Steering cover', 'Seat covers', 'Floor mats'],
                'colors': ['Black', 'Gray', 'Beige']
            }
        }
    }
}


# Flatten the data into a list of dictionaries
flat_data = []
for brand, models in car_data.items():
    for model, types in models.items():
        for car_type, details in types.items():
            for color in details['colors']:
                flat_data.append({
                    'Brand': brand,
                    'Model': model,
                    'Type': car_type,
                    'Color': color,
                    'Accessories': ', '.join(details['accessories'])
                })

# Create a pandas DataFrame
df = pd.DataFrame(flat_data)

# Write the DataFrame to an Excel file
df.to_excel('car_data.xlsx', index=False)