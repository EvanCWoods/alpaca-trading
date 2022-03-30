const { Model, DataTypes } = require("sequelize");
const sequelize = require("../config/connection");

class Trend extends Model {}

Trend.init(
  {
    id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      autoIncrement: true,
    },
    date: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    high: {
      type: DataTypes.DOUBLE,
      allowNull: false,
    },
    low: {
      type: DataTypes.DOUBLE,
      allowNull: false,
    },
    open: {
      type: DataTypes.DOUBLE,
      allowNull: false,
    },
    close: {
      type: DataTypes.DOUBLE,
      allowNull: false,
    },
    volume: {
      type: DataTypes.STRING,
      allowNull: false,
    }
  },
  {
    sequelize,
    freezeTableName: true,
    underscored: true,
    modelName: "trend",
  }
);

module.exports = Trend;