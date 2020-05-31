# HypeCache
A web-based store that removes that hard-to-get item worry! This site offers limited items to those who missed out
(at a slight premium of course). Or trusted sellers can apply to sell with us.
Users can add items to their cart and checkout securely using stripe! No payment information is shared with us!

## Mockups
[Link to mockup pdf within repo](../master/HypeCache.pdf)

## UX
The homepage brings users straight to the action, giving a filter, a full search bar and all the products they could desire.
User need only hover over the items for a more detailed description and, if it takes their fancy, one click takes them to the detailed product
and add-to-cart view.

To add an item to cart, users must create an account. This is made obvious by the redirect to the login page when un-authorised users try
adding to cart. All accounts and passwords are secured and stored only as hashes in the SQL database. If you have checked out before,
you'll be told to confirm your previously saved delivery information, or create a new address. Once confirmed, stripe handles the checkout
and payment, a webhook checks for successful payment and then you are sent the details via email(Stripe doesn't send emails in test).
More proactively, you can head to your profile view (clicking your name at the top) and view all your orders there! This is also where
the site owner (superuser)can see all orders. You're done! log out and wait for your items to be delivered! 

### User Stories
  * I just missed out on the lastest limited item and would like a safe site to purchase it from. Using Stripe, I can be sure that my
  payment information is safe. And, being on mobile, I can even use Apple Pay!
  * I don't want the hassle of camping or waiting for the next release. I check Hypecache for all the items I want.
  * I'm a trusted seller in the market and would like to put some items for sale on Hypecache. I send a request from the contact form
  and I'm now a Staff member on the site, This opens the possibility of making posts to the site, I'm able to add a picture and all the 
  details I could want.

## Features

  * Allows users to view and purchase items from the store.
  * Create an account by clicking on 'Login' in the nav bar and then the 'Create Account' text to fill out your user form.
  * As a Trusted seller you can click 'New Post' to add new items to the store.
  * As a customer, you can check your order from the account page. And even view your Stripe reciept.
  * Edit or delete posts, set items as 'Not for sale' or increase the quantity if you have more than one!
  * Infinite Pagination on the home and filter pages, takes away the need to continously click 'next page'. It's done for you!
  * Your Cart is tied to your account so feel free to leave it for another day, it'll still be there!
  * Stripe webhook integration makes sure that payments are completed before any orders are marked as confirmed.
  * Staff can see all 'Not for sale' posts on the home page (for reuploading or deletion). While they are invisible to members.
  * Reset your password or update your email in the accounts page!

### Future Ideas
  * Add page for staff to easily see all deliveries they need to make and see how much theyve made overall.
  * Add more checks for item quantity so that two users checking out at the same time don't cause errors.
  * Add proper staff forms that display for the super user on-site.
  * Multiple picture uploads 

## Technologies Used
This project uses:
  * HTML 5
  * CSS
  * Javascript/ Jquery to improve UX. Example: Add to cart and increase .Qty buttons.
  * Python 3.6.6 (heroku)
  * [Bootstrap 4.5](https://getbootstrap.com/) - Used for simple styling and layout.
  * [Django 2.2.12](https://www.djangoproject.com/) - Python web framework.
  * [Amazon AWS S3](https://aws.amazon.com/) - Used for image uploading and storing.
  * [Heroku](https://heroku.com/) - Used to host the site.


## Deployment

This site is deployed [HERE](https://hypecache.herokuapp.com/) on Heroku.  
Heroku config variables are used in order to conceal variables used for security.

I have created a test staff user here:
code : codeinstitute
This is to allow testing of staff only features, such as posting items for sale.

## Testing
  * Went through the site with my tutor checking major flaws there could be with the site. For example, checking authentication
  was working properly and did not allow non users into parts of the site that they shouldnt be.
  * went through the user stories to make sure that the site worked as intended.
  * Forwarded site to users without giving them context of the site to see if the ux and ui was easily understood. 
  Which it seemed to be.
  * Tested personally with different user types to make sure there was no UX hiccups

## Credits

### Images
Images taken by me, taken from [Ssense](https://ssense.com/) or [Dior](https://heroku.com/) for the Banner image.
Icons from [iconmonstr](https://iconmonstr.com/)

### Product information
One product taken from [Omega Wiki](https://en.wikipedia.org/wiki/Omega_Speedmaster)
