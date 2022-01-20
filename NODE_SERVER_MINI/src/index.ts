import puppeteer from 'puppeteer'
import fs from 'fs'
async function autoScroll(page) {
	await page.evaluate(async () => {
		await new Promise<void>((resolve, _) => {
			let totalHeight = 0
			let distance = 500
			let timer = setInterval(() => {
				let scrollHeight = document.body.scrollHeight
				window.scrollBy(0, distance)
				totalHeight += distance

				if (totalHeight >= scrollHeight) {
					clearInterval(timer)
					resolve()
				}
			}, 100)
		})
	})
}

const writeFiles = async (url, fileName) => {
	try {
		const browser = await puppeteer.launch({
		})
		const [page] = await browser.pages()
		const urlList = ['']
		// #video-count
		await page.goto(
			`https://www.youtube.com/results?search_query=${fileName}`,
			{ waitUntil: 'networkidle2' }
		)
		const count = await page.$eval('#video-count', (el) =>
			Number(el.innerHTML.split(' ')[0])
		)
		console.log(count)

		await page.goto(url, {
			waitUntil: 'networkidle2',
		})

		await page.setViewport({
			width: 1200,
			height: 800,
		})

		console.log({ fileName })
		for (let i = 1; i < count; i++) {
			await autoScroll(page)
			const video_url_selector = `#items > ytd-grid-video-renderer:nth-child(${i}) > div > div > div > h3 > a`
			await page.waitForSelector(video_url_selector)
			// @ts-ignore
			const video_url: string = await page.$eval(
				video_url_selector,
				(el: any) => el.href
			)
			urlList.push(video_url)
			console.log(video_url)
		}
		console.log(urlList.length)
		const save =  fs.createWriteStream(fileName+'.txt', { flags: 'w' })
		urlList.forEach(async (video_url: any) => {
		  save.write(video_url + '\n')
		})
		await browser.close()
	} catch (error) {
		console.log(error)
	}
}

const readFiles = async () => {
	try {
		fs.readFile('youtube_up.json', 'utf-8', (err, data) => {
			if (err) console.log(err)
			const json = JSON.parse(data)
			Object.keys(json).forEach(async (key) => {
				await writeFiles(json[key], key)
			})
		})
	} catch (error) {
		console.log(error)
	}
}
readFiles()
