from src.tests.sublog_test_utils import SublogTestCase


class PreviewMarkdownTests(SublogTestCase):
    def markdown_response(self, markdown):
        post_data = {'text': markdown}

        response = self.client.post('/markdown/', data=post_data)
        self.assertEquals(200, response.status_code)
        self.assertEquals('text/html', response['Content-Type'])
        return response.content

    def test_empty_markdown(self):
        response = self.markdown_response('')
        self.assertEquals(0, len(response))

    def test_minimal_markdown(self):
        response = self.markdown_response('**bold**')
        self.assertEquals("<p><strong>bold</strong></p>", response)

    def test_escapes_html(self):
        response = self.markdown_response('<h2>huge</h2>')
        self.assertEquals("<p>&lt;h2&gt;huge&lt;/h2&gt;</p>", response)

    def test_escapes_script(self):
        response = self.markdown_response("""## heading\n text <script>alert('hello');</script>""")
        self.assertEquals("<h2>heading</h2>\n<p>text &lt;script&gt;alert(&#39;hello&#39;);&lt;/script&gt;</p>",
                          response)

    def test_image_link(self):
        input_content = self.test_file_content('image_link_input.md')
        expected = self.test_file_content('image_link_expected.html')
        self.compare_contents(expected, self.markdown_response(input_content))

    def test_full_markdown(self):
        input_content = self.test_file_content('full_markdown_input.md')
        expected = self.test_file_content('full_markdown_expected.html')
        self.compare_contents(expected, self.markdown_response(input_content))
