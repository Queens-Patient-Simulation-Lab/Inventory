import { library, dom, config } from "@fortawesome/fontawesome-svg-core";
config.autoAddCss = false // needed for CSP

// import any used icons here
import { faCamera } from "@fortawesome/free-solid-svg-icons";
library.add(faCamera);


dom.watch();