# Hexashop
The Clothing App is a user-friendly and stylish online platform that offers a wide range of trendy clothing items for fashion-conscious shoppers. Whether you're looking for casual wear, formal attire, or accessories to complete your look, our app has you covered.

## Screenshot

![Screenshot from 2023-08-07 17-40-11](https://github.com/saitr/Clothing-App/assets/64057564/529d1bf3-882e-4be5-9352-0afef49eef5e)


## Features

1. **Extensive Collection:** Browse through a diverse collection of clothing items for men, women, and kids, carefully curated to suit various tastes and preferences.

2. **Seamless Shopping Experience:** Enjoy a smooth and intuitive shopping experience with easy navigation, search functionality, and user-friendly filters.

3. **Wishlist and Favorites:** Save your favorite items to your wishlist, so you can easily find and purchase them later.

4. **Personalized Recommendations:** Discover new styles and fashion trends tailored to your interests through personalized recommendations based on your browsing history.

5. **Real-Time Inventory:** Stay updated on item availability with real-time inventory tracking, so you won't miss out on your favorite pieces.

6. **User Accounts:** Create an account to track your orders, manage your wishlist, and receive exclusive offers and discounts.

## How to Get Started

1. **Create an Account:** Sign up for a free account to access personalized features and start shopping.

2. **Browse and Shop:** Explore our extensive collection and add your favorite items to your cart.

3. **Checkout and Payment:** Securely complete your purchase with our seamless checkout process.

4. **Track Your Order:** Once your order is placed, you can track its status and receive updates on delivery.

## Installation

Follow these steps to set up and install the Clothing App:

1. **Prerequisites:**
   - Make sure you have Python 3.9 or higher installed on your system.
   - [Optional] It's recommended to use a virtual environment to keep the project dependencies isolated. You can use `venv`, `virtualenv`, or `conda` for this purpose.

2. **Clone the Repository:**
   Clone the Clothing App repository to your local machine using the following command: 


3. **Navigate to the Project Directory:**
Change your current working directory to the cloned project folder:

4. **Install Dependencies:**
Install the required Python dependencies using `pip3`. It's recommended to use a virtual environment at this point if you have set one up.The commands are as such **pip3 install -r requirements.txt** to install the requirements before that activate virtual_env by using the command **source clothing-env/bin/activate** ( for linux and mac )

5. **Run the App:**
Finally, run the Clothing App using the following command: **python3 manage.py runserver**


## Installation or Setup Through Docker 

1. **Docker Image:** Pull the docker image by the executing the following command in the local integrated terminal **docker pull saitreddy/clothing-app:hexashop**
2. The above command pull the image from docker hub and then check the image with command **docker images**
3. If the image exists then run the image by the command **docker run -d -p 8000:8000 image_id**, so here in the place of the port number you can port numbers such as the 8000:8001 etc and then copy the image_id and paste it.
4. Now the container will be running and you can check it by using the command **docker ps**, then copy the port and paste it in the google search bar.

