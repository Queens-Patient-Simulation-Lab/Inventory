import { library, dom, config } from "@fortawesome/fontawesome-svg-core";
config.autoAddCss = false // needed for CSP

// import any used icons here
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
library.add(faTrashAlt);


dom.watch();