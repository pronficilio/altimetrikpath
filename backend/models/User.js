const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
  },
  cv: {
    type: String,
  },
  original_cv: {
    type: String,
  },
  experience: [String],
  skills: [String],
  education: [String],
  certifications: [Object],
  projects: [String],
  languages: [String],
});

module.exports = mongoose.model('User', UserSchema);
