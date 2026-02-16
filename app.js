require("dotenv").config();
const express = require("express");
const app = express();
const passport = require("passport");
require("./config/passport")(passport);


app.use(session({
    secret : process.env.SESSION_SECRET,
    resave : false,
    saveUninitialized : true,
    cookie: {
        expires : Date.now() + 7*24*60*60*1000,
        maxAge : 7*24*60*60*1000,
        httpOnly : true,
    }
  })
);

app.use(passport.initialize());
app.use(passport.session());

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

app.set("views", "views");
app.set("view engine", "ejs");

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));

app.use("/auth", require("./routes/auth"));

// app.get("/", (req, res) => {
//   res.send("Hello, world!");
// });