const {Router} = require("express");
const router = Router();

router.get("/sign-up", require("../controllers/auth").getsignup);
router.post("/sign-up", require("../controllers/auth").postsignup);
router.get("/login", require("../controllers/auth").getlogin);
router.post("/login", require("../controllers/auth").postlogin);
router.get("/logout", require("../controllers/auth").getlogout);

module.exports = router;