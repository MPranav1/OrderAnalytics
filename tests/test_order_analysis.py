
import unittest
import pandas as pd

class TestOrderAnalysis(unittest.TestCase):

    def setUp(self):
        # Load the actual dataset
        self.df = pd.read_csv('orders.csv')
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])

    def test_monthly_revenue(self):
        self.df['month'] = self.df['order_date'].dt.to_period('M')
        monthly_revenue = self.df.groupby('month').apply(
            lambda x: (x['product_price'] * x['quantity']).sum()
        ).reset_index(name='total_revenue')
        self.assertEqual(
            monthly_revenue['total_revenue'].sum(),
            self.df['product_price'].mul(self.df['quantity']).sum()
        )  # Total revenue

    def test_product_revenue(self):
        product_name = self.df['product_name'].iloc[0]  # Taking the first product name for example
        product_revenue = self.df.groupby('product_name').apply(
            lambda x: (x['product_price'] * x['quantity']).sum()
        ).reset_index(name='total_revenue')
        expected_revenue = self.df[self.df['product_name'] == product_name].apply(
            lambda x: x['product_price'] * x['quantity'], axis=1
        ).sum()
        self.assertEqual(
            product_revenue.loc[product_revenue['product_name'] == product_name, 'total_revenue'].values[0],
            expected_revenue
        )

    def test_customer_revenue(self):
        customer_revenue = self.df.groupby('customer_id').apply(
            lambda x: (x['product_price'] * x['quantity']).sum()
        ).reset_index(name='total_revenue')
        customer_id = self.df['customer_id'].iloc[0]  # Taking the first customer_id for example
        expected_revenue = self.df[self.df['customer_id'] == customer_id].apply(
            lambda x: x['product_price'] * x['quantity'], axis=1
        ).sum()
        self.assertEqual(
            customer_revenue.loc[customer_revenue['customer_id'] == customer_id, 'total_revenue'].values[0],
            expected_revenue
        )

    def test_top_customers(self):
        customer_revenue = self.df.groupby('customer_id').apply(
            lambda x: (x['product_price'] * x['quantity']).sum()
        ).reset_index(name='total_revenue')
        top_customers = customer_revenue.nlargest(10, 'total_revenue')
        top_customer_id = customer_revenue.nlargest(1, 'total_revenue').iloc[0]['customer_id']
        expected_top_customer_id = self.df.groupby('customer_id').apply(
            lambda x: (x['product_price'] * x['quantity']).sum()
        ).nlargest(1).index[0]
        self.assertEqual(top_customer_id, expected_top_customer_id)

if __name__ == '__main__':
    unittest.main()
