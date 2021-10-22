from fpdf import FPDF


class PDF(FPDF):

    def body(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Page" + str(self.page_no()), 0, 0, "C")


def convertor_to_pdf(data, path, verbose):
    pass


if __name__ == '__main__':
    convertor_to_pdf("", "", None)