exports.login = (req, res) => {
  res.json({ message: 'Login successful', user: req.user });
};

exports.logout = (req, res) => {
  req.logout(() => {
    res.json({ message: 'Logged out successfully' });
  });
};