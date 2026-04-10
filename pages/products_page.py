from playwright.sync_api import Page, expect

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, merchant_id):
        self.page.goto(f"https://qa-mdashboard.dev.gokwik.in/gk-pages/store/{merchant_id}/products")

    def create_product(self, name):
        self.page.get_by_role("button", name="Create Product").click()
        self.page.locator("input[name='productName']").fill(name)
        self.page.get_by_role("button", name="Save").click()

        expect(self.page.get_by_text(name)).to_be_visible()

    def search_product(self, name):
        self.page.locator("input[placeholder='Search']").fill(name)
        self.page.keyboard.press("Enter")

    def update_product(self, old_name, new_name):
        self.page.get_by_text(old_name).click()
        self.page.locator("input[name='productName']").fill(new_name)
        self.page.get_by_role("button", name="Save").click()

        expect(self.page.get_by_text(new_name)).to_be_visible()

    def delete_product(self, name):
        self.page.get_by_text(name).click()
        self.page.get_by_role("button", name="Delete").click()
        self.page.get_by_role("button", name="Confirm").click()

        expect(self.page.get_by_text(name)).not_to_be_visible()

    def negative_create(self):
        self.page.get_by_role("button", name="Create Product").click()
        self.page.get_by_role("button", name="Save").click()

        expect(self.page.get_by_text("required")).to_be_visible()