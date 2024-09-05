const puppeteer = require("puppeteer");
const dotenv = require("dotenv");
dotenv.config();
codigoEmpregador = process.env.CODIGOEMPREGADOR;
pin = process.env.PIN;
const urlSolides = "https://app.tangerino.com.br/Tangerino/pages/LoginPage";
(async () => {
  // Inicializa o navegador
  const browser = await puppeteer.launch({ headless: false }); // Use headless: false para visualizar o navegador
  const page = await browser.newPage();

  // Navega para o site de login
  await page.goto(urlSolides);

  // Clica no botão de colaborador

  await page.evaluate(() => {
    const links = document.querySelectorAll("ul.login-abas li a.login-aba");
    for (const link of links) {
      if (link.textContent.includes("Colaborador")) {
        link.click();
        break;
      }
    }
  });
  await page.waitForNavigation();
  // Preenche o formulário de login
  await page.type("#idd", codigoEmpregador); // username
  await page.type("#id10", pin); // password
  // await page.click("#id11");
  // Aguarda a navegação para a próxima página
  await page.waitForNavigation();

  // Fecha o navegador
  // await browser.close();
})();