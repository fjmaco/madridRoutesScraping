import scrapy
import re
from scrapy import Request
from prueba.items import ItinerarioItem


class MadridRoutesSpider(scrapy.Spider):
    name = "madrid_routes"

    BASE_URL = "https://turismomadrid.es"
    ROUTES_URL = BASE_URL + "/es/rutas.html"
    ALL_DB = False

    custom_settings = {
        "ITEM_PIPELINES": {"prueba.pipelines.ElasticsearchPipeline": 300},
        "CONCURRENT_REQUESTS": 8,
    }

    def start_requests(self):
        req = Request(
            url=self.ROUTES_URL,
            callback=self.parse_etapas,
        )
        yield req

    def parse_etapas(self, response):
        etapas = response.xpath(
            '//div[@id="region3wrap"]//div//a[contains(@href,"rutas")]/@href'
        ).getall()

        if self.ALL_DB:
            for etapa in etapas:
                req = Request(
                    url=self.BASE_URL + etapa,
                    callback=self.parse_etapa,
                )
                yield req
        else:
            req = Request(
                url=self.BASE_URL + etapas[0],
                callback=self.parse_etapa,
            )
            yield req

    def parse_etapa(self, response):
        main_etapa_title = response.xpath('//h1[@class="titulo-etapa"]/text()').get()
        main_etapa_description = response.xpath(
            '//div[contains(@class,"descripcion-etapa")]/p/text()'
        ).get()
        main_etapa_image = response.xpath(
            '//div[contains(@class,"descripcion-etapa")]/../div/img/@src'
        ).get()
        main_etapa_distance = response.xpath(
            '//div[contains(@class,"dato-etapa")]/span/../..//span[contains(text(),"KM")]/text()'
        ).get()
        main_etapa_total_routes = response.xpath(
            '//div[contains(@class,"dato-etapa")]/span/../..//span[contains(text(),"etapa")]/text()'
        ).get()
        main_etapa_duration = response.xpath(
            '//div[contains(@class,"dato-etapa")]/span/../..//span[contains(text(),"h")]/text()'
        ).get()
        gpx_link = (
            self.BASE_URL
            + response.xpath(
                '//a[contains(@class,"download")]/../a[contains(text(),"GPX")]/@href'
            ).get()
        )
        kmz_link = (
            self.BASE_URL
            + response.xpath(
                '//a[contains(@class,"download")]/../a[contains(text(),"KMZ")]/@href'
            ).get()
        )

        main_etapa_details = {
            "main_etapa_title": main_etapa_title,
            "main_etapa_description": main_etapa_description,
            "main_etapa_image": main_etapa_image,
            "main_etapa_distance": main_etapa_distance,
            "main_etapa_total_routes": main_etapa_total_routes,
            "main_etapa_duration": main_etapa_duration,
            "gpx_link": gpx_link,
            "kmz_link": kmz_link,
        }
        mainEtapa = {
            "id": main_etapa_title,
            "object": "main_etapa",
            "details": main_etapa_details,
        }
        yield ItinerarioItem(mainEtapa)

        rutas = response.xpath(
            '//div[@id="region3wrap"]//div//a[contains(@href,"rutas")]/@href'
        ).getall()

        if self.ALL_DB:
            for route in rutas:
                req = Request(
                    url=self.BASE_URL + route,
                    callback=self.parse_routes,
                )
                req.meta["_main_etapa_details"] = main_etapa_details
                yield req
        else:
            req = Request(
                url=self.BASE_URL + rutas[0],
                callback=self.parse_routes,
            )
            req.meta["_main_etapa_details"] = main_etapa_details
            yield req

    def parse_routes(self, response):
        main_etapa_details = response.meta["_main_etapa_details"]
        main_etapa_title = main_etapa_details["main_etapa_title"]

        route_number = response.xpath('//h3[@class="etapa-titulo"]/text()').get()
        route_name = response.xpath('//h1[@class="nivel2-titulo"]/text()').get()
        route_description_all = response.xpath(
            '//div[contains(@class,"descripcion-etapa")]/p/text()'
        ).getall()
        route_description = " ".join(route_description_all)
        gpx_link = (
            self.BASE_URL
            + response.xpath(
                '//a[contains(@class,"download")]/../a[contains(text(),"GPX")]/@href'
            ).get()
        )
        kmz_link = (
            self.BASE_URL
            + response.xpath(
                '//a[contains(@class,"download")]/../a[contains(text(),"KMZ")]/@href'
            ).get()
        )

        route_details = {
            "route_number": route_number,
            "route_name": route_name,
            "route_description": route_description,
            "gpx_link": gpx_link,
            "kmz_link": kmz_link,
        }

        routeDetails = {
            "id": main_etapa_title + "_" + route_number,
            "object": "route_details",
            "details": route_details,
        }
        yield ItinerarioItem(routeDetails)

        itinerarios = response.xpath(
            '//div[@id="region3wrap"]//div//a[contains(@href,"etapa")]/@href'
        ).getall()
        if self.ALL_DB:
            for route in itinerarios:
                req = Request(
                    url=self.BASE_URL + route,
                    callback=self.parse_itinerarios,
                )
                req.meta["_main_etapa_details"] = main_etapa_details
                req.meta["_route_details"] = route_details
                yield req
        else:
            req = Request(
                url=self.BASE_URL + itinerarios[0],
                callback=self.parse_itinerarios,
            )
            req.meta["_main_etapa_details"] = main_etapa_details
            req.meta["_route_details"] = route_details
            yield req

    def parse_itinerarios(self, response):
        main_etapa_details = response.meta["_main_etapa_details"]
        route_details = response.meta["_route_details"]

        main_etapa_title = main_etapa_details["main_etapa_title"]
        route_number = route_details["route_number"]

        itinerary_title = response.xpath('//h1[@class="nivel2-titulo"]/text()').get()
        itinerary_distance = response.xpath(
            '//div[contains(@class, "distancia-ruta")]//span/text()'
        ).get()
        itinerary_details = response.xpath(
            '//div[contains(@class,"descripcion-etapa")]/p/text()'
        ).getall()
        itinerary_description = itinerary_details[0]
        itinerary_path = itinerary_details[1]

        step_by_step = response.xpath(
            '//div[contains(@class,"large-bottom")]/div/div/../../div'
        )

        stepsList = []
        for step in step_by_step:
            step_name = step.xpath('.//div[@id="texto"]//text()').get()
            step_description = step.xpath(
                './/div[contains(@class,"descripcion-etapa")]/p[1]/text()'
            ).get()
            image_long = step.xpath(
                './/div[contains(@style,"background-image")]/@style'
            ).get()
            if image_long is not None:
                image_link = re.search("(?P<url>https?://[^\s]+)", image_long).group(
                    "url"
                )
            else:
                image_link = ""
            stepObject = {
                "step_name": step_name,
                "step_description": step_description,
                "image_link": image_link,
            }
            stepsList.append(stepObject)

        itinerario_info = {
            "itinerary_title": itinerary_title,
            "itinerary_distance": itinerary_distance,
            "itinerary_description": itinerary_description,
            "itinerary_path": itinerary_path,
            "step_by_step": stepsList,
        }

        itinerarioDetails = {
            "id": main_etapa_title + "_" + route_number + "_" + itinerary_title,
            "object": "itinerario_details",
            "details": itinerario_info,
        }
        yield ItinerarioItem(itinerarioDetails)
