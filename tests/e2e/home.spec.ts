import { test, expect, type Locator } from '@playwright/test'

test.describe('when a user navigates to the homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('has title', async ({ page }) => {
    await expect(page).toHaveTitle(/JSON Validator/)
  })

  test('has heading', async ({ page }) => {
    await page.getByText('JSON Validator').click()
    await expect(page).toHaveURL('https://github.com/tjmaynes/json-validator-app')
  })

  test('has footer', async ({ page }) => {
    await page.getByText('TJ Maynes').click()
    await expect(page).toHaveURL('https://tjmaynes.com/')
  })

  test('has initial state set', async ({ page }) => {
    await expect(page.getByText('🤘')).toBeVisible()
    await expect(page.getByText('👍')).not.toBeVisible()
    await expect(page.getByText('👎')).not.toBeVisible()

    await expect(page.getByLabel('Pretty print')).toBeDisabled()
    await expect(page.getByLabel('Compress')).toBeDisabled()
    await expect(page.getByLabel('Copy')).toBeDisabled()
    await expect(page.getByLabel('Clear')).toBeDisabled()
  })

  test.describe('other functionality', () => {
    const expected = '[{"hello" : "world"}, {"green": "red"}]'
    let placeholderText: Locator

    test.beforeEach(async ({ page }) => {
      placeholderText = page.getByPlaceholder('Type or paste your json here...')

      await placeholderText.fill(expected)

      await expect(page.getByLabel('Copy')).not.toBeDisabled()
      await expect(page.getByLabel('Clear')).not.toBeDisabled()
      await expect(page.getByLabel('Compress')).not.toBeDisabled()
      await expect(page.getByLabel('Pretty print')).not.toBeDisabled()
    })

    test('should copy json to clipboard when copy button clicked', async ({
      page,
      browserName,
    }) => {
      await page.getByLabel('Copy').click()

      if (!['webkit', 'Desktop Safari', 'Mobile Safari'].includes(browserName)) {
        const handle = await page.evaluateHandle(() => navigator.clipboard.readText())
        const clipboardContent = await handle.jsonValue()
        expect(clipboardContent).toEqual(expected)
      }

      await expect(page.getByText('Copied to clipboard!')).toBeVisible()
    })

    test('should compress json when compress button clicked', async ({ page }) => {
      await expect(placeholderText.getByText(expected)).toBeVisible()

      await page.getByLabel('Compress').click()

      await expect(placeholderText.getByText('[{"hello":"world"},{"green":"red"}]')).toBeVisible()

      await expect(page.getByText('Compressed!')).toBeVisible()
    })

    test('should clear textarea when clear button clicked', async ({ page }) => {
      await expect(placeholderText.getByText(expected)).toBeVisible()

      await page.getByLabel('Clear').click()

      await expect(placeholderText.getByText(expected)).not.toBeVisible()
    })

    test('should prettify unpretty json input when pretty button clicked and input is valid', async ({
      page,
    }) => {
      const expectedOutput = `[
   {
      "hello": "world"
   },
   {
      "green": "red"
   }
]`

      await placeholderText.fill('[ {"hello" : "world"}, { "green": "red"}]')

      await expect(page.getByText('👍')).toBeVisible()

      await page.getByLabel('Pretty print').click()

      await expect(placeholderText.getByText(expectedOutput)).toBeVisible()

      await expect(page.getByText('👍')).toBeVisible()
      await expect(page.getByText('Prettified!')).toBeVisible()
    })

    test('pretty button is disabled when input is invalid ', () => {})
  })
})
