from playwright.sync_api import Page, expect
import re


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, email, password, otp):
        self.page.goto("https://qa-mdashboard.dev.gokwik.in/")

        email_input = self.page.get_by_placeholder("example@email.com")
        expect(email_input).to_be_visible()
        email_input.fill(email)

        self.page.get_by_role("button", name="Next").click()

        password_input = self.page.locator("input[type='password']")
        expect(password_input).to_be_visible()
        password_input.fill(password)

        self.page.get_by_role("button", name="Next").click()

        expect(self.page.get_by_text("Resend OTP")).to_be_visible(timeout=10000)

        inputs = self.page.locator("input:visible")
        count = inputs.count()
        print("OTP inputs found:", count)

        if count == 1:
            inputs.first.fill(otp)
        else:
            for i in range(min(len(otp), count)):
                inputs.nth(i).fill(otp[i])

        next_btn = self.page.get_by_role("button", name="Next")
        expect(next_btn).to_be_visible(timeout=10000)
        next_btn.click()

        expect(self.page).to_have_url(re.compile("dashboard"), timeout=30000)


    def switch_merchant(self, merchant_id):
        expect(self.page).to_have_url(re.compile("dashboard"))


        dropdown = self.page.get_by_role(
            "button",
            name=re.compile("qa.gokwik", re.IGNORECASE)
        )
        expect(dropdown).to_be_visible(timeout=10000)
        dropdown.click()


        modal = self.page.locator("text=Search merchant or merchant id")
        expect(modal).to_be_visible(timeout=10000)


        modal_container = self.page.locator("div").filter(
            has_text="Search merchant or merchant id"
        )

        search_input = modal_container.locator("input").first
        expect(search_input).to_be_visible(timeout=10000)

        search_input.click()
        search_input.fill("")
        search_input.fill(merchant_id)

        # 4. WAIT FOR FILTER
        self.page.wait_for_timeout(1500)

        # 5. SELECT ONLY VISIBLE RESULTS (NOT GOOGLE INPUT)
        merchant_option = modal_container.get_by_text(merchant_id).first
        expect(merchant_option).to_be_visible(timeout=10000)
        merchant_option.click()

        # 6. CONFIRM
        set_button = self.page.get_by_role("button", name="Set Merchant")
        expect(set_button).to_be_visible(timeout=10000)
        set_button.click()

        # 7. FINAL VALIDATION
        expect(
            self.page.get_by_text(merchant_id)
        ).to_be_visible(timeout=20000)