import pytest
from playwright.sync_api import sync_playwright, expect
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.data import *
import time


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        yield page
        browser.close()


def test_crud_flow(page):
    login = LoginPage(page)
    products = ProductsPage(page)

    # Login + merchant switch
    login.login(EMAIL, PASSWORD, OTP)
    login.switch_merchant(MERCHANT_ID)

    # Navigate to products
    products.navigate(MERCHANT_ID)

    # ---------------- CREATE ---------------- #
    products.create_product(PRODUCT_NAME)
    expect(page.get_by_text(PRODUCT_NAME)).to_be_visible(timeout=15000)

    # ---------------- READ ---------------- #
    products.search_product(PRODUCT_NAME)
    expect(page.get_by_text(PRODUCT_NAME)).to_be_visible(timeout=10000)

    # ---------------- UPDATE ---------------- #
    products.update_product(PRODUCT_NAME, UPDATED_NAME)

    # Validate update
    products.search_product(UPDATED_NAME)
    expect(page.get_by_text(UPDATED_NAME)).to_be_visible(timeout=10000)

    # ---------------- DELETE ---------------- #
    products.delete_product(UPDATED_NAME)

    # Validate deletion
    products.search_product(UPDATED_NAME)
    expect(page.get_by_text(UPDATED_NAME)).not_to_be_visible(timeout=10000)


def test_negative_scenario(page):
    login = LoginPage(page)
    products = ProductsPage(page)

    login.login(EMAIL, PASSWORD, OTP)
    login.switch_merchant(MERCHANT_ID)

    products.navigate(MERCHANT_ID)

    # Try creating without mandatory field (Title)
    products.negative_create()

    # Validate error message
    expect(page.get_by_text("Title is required")).to_be_visible(timeout=10000)