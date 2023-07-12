import json
import logging
import time
from typing import Generator
from typing import Optional

import requests
from retry import retry

from bomsquad.vulndb.config import config
from bomsquad.vulndb.model.cpe import CPE
from bomsquad.vulndb.model.cve import CVE

logger = logging.getLogger(__name__)


class NVD:
    CVE_STEM = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    CPE_STEM = "https://services.nvd.nist.gov/rest/json/cpes/2.0"

    @retry(Exception, backoff=1, tries=10, max_delay=5, logger=logger)
    def vulnerabilities(
        self, offset: int = 0, limit: Optional[int] = None, **kwargs: str
    ) -> Generator[CVE, None, None]:
        total_results = 0
        while True:
            url = f"{self.CVE_STEM}?startIndex={offset}"
            headers = {"Accept": "application/json"}
            if config.nvd_api_key:
                headers["apiKey"] = config.nvd_api_key

            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                r.raise_for_status()

            jres = json.loads(r.text)
            if jres["totalResults"] > 0:
                logger.info(
                    f"Materializing {offset}-{offset + jres['resultsPerPage']} / {jres['totalResults']}"
                )
            for jso in jres["vulnerabilities"]:
                yield CVE.parse_obj(jso["cve"])
                total_results += 1
                offset += 1
                if limit and total_results >= limit:
                    return

            if jres["resultsPerPage"] <= 0:
                return

            time.sleep(config.request_delay)

    @retry(Exception, backoff=1, tries=10, max_delay=5, logger=logger)
    def products(self, offset: int = 0, limit: Optional[int] = None) -> Generator[CPE, None, None]:
        total_results = 0
        while True:
            url = f"{self.CPE_STEM}?startIndex={offset}"
            headers = {"Accept": "application/json"}
            if config.nvd_api_key:
                headers["apiKey"] = config.nvd_api_key

            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                r.raise_for_status()

            jres = json.loads(r.text)
            if jres["totalResults"] > 0:
                logger.info(
                    f"Materializing {offset}-{offset + jres['resultsPerPage']} / {jres['totalResults']}"
                )
            for jso in jres["products"]:
                yield CPE.parse_obj(jso["cpe"])
                total_results += 1
                offset += 1
                if limit and total_results >= limit:
                    return

            if jres["resultsPerPage"] <= 0:
                return

            time.sleep(config.request_delay)