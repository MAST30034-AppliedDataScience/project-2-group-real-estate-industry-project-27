import matplotlib.pyplot as plt

def rent_by_suburb (df, postcode):
    '''Draw a box plot of the rental prices in the given postcode'''
    filtered_df = df[df['postcode'] == postcode]
    plt.boxplot(filtered_df['price (AUD per week)'], vert=False)

    plt.title(f'Rental Prices in Postcode {postcode}')
    plt.xlabel('Price (AUD per week)')
    plt.grid(True)
    plt.show()