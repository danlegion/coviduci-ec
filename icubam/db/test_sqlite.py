import os
import time

from absl.testing import absltest
from icubam.db import sqlite
import sqlite3
import tempfile

class SQLiteDBTest(absltest.TestCase):

  def test_init(self):
    with tempfile.TemporaryDirectory() as tmp_folder:
        sqldb = sqlite.SQLiteDB(os.path.join(tmp_folder, "test.db"))

  def test_icu_creation(self):
    with tempfile.TemporaryDirectory() as tmp_folder:
        sqldb = sqlite.SQLiteDB(os.path.join(tmp_folder, "test.db"))
        sqldb.upsert_icu("ICU1", "dep1", "city1", 3.44, 42.3, "0102")
        icus = sqldb.get_icus()
        self.assertEqual(icus[icus["icu_name"] == "ICU1"].iloc[0]["dept"], "dep1")

        sqldb.upsert_icu("ICU2", "dep2", "city2", 3.44, 42.3)
        icus = sqldb.get_icus()
        self.assertEqual(icus[icus["icu_name"] == "ICU2"].iloc[0]["dept"], "dep2")

        sqldb.upsert_icu("ICU1", "dep3", "city3", 3.44, 42.3, "0103")
        icus = sqldb.get_icus()
        self.assertEqual(icus[icus["icu_name"] == "ICU1"].iloc[0]["dept"], "dep3")
        self.assertEqual(icus[icus["icu_name"] == "ICU1"].iloc[0]["telephone"], "0103")



  def test_user_creation(self):
    with tempfile.TemporaryDirectory() as tmp_folder:
        sqldb = sqlite.SQLiteDB(os.path.join(tmp_folder, "test.db"))

        # Make sure you can't add a user with non-existant ICU
        with self.assertRaises(ValueError):
          sqldb.add_user("ICU1", "Bob", "+33698158092", "Chercheur")

        # Check normal insertion
        sqldb.upsert_icu("ICU1", "dep1", "city1", 3.44, 42.3, "0102")
        sqldb.add_user("ICU1", "Bob", "+33698158092", "Chercheur")

        with self.assertRaises(sqlite3.IntegrityError):
          sqldb.add_user("ICU1", "Bob", "+33698158092", "Chercheur")
        users = sqldb.get_users()

  # def test_bedcount_update(self):
  #   tmp_folder = self.create_tempdir()
  #   sqldb = SQLiteDB(os.path.join(tmp_folder, "test.db"))

  #   # Make sure you can't insert without a valid icu_id
  #   with self.assertRaises(ValueError):
  #     sqldb.update_bedcount(1, "test", 10, 9, 8, 7, 6, 5, 4)
  #   sqldb.upsert_icu("ICU1", "dep1", "city1", 3.44, 42.3, "0102")
  #   sqldb.upsert_icu("ICU2", "dep1", "city1", 3.44, 42.3, "0102")

  #   # Generate some bed updates:
  #   for i in [1, 2]:
  #     for j in range(10):
  #       time.sleep(0.5)
  #       sqldb.update_bedcount(i, "test", 10, 9, 8, 7, 6, 5, 4)
  #   bedcount = sqldb.get_bedcount()
  #   self.assertLen(bedcount, 2)

  #   # Make sure the returned updates are the most recent
  #   for i in [1, 2]:
  #     res = sqldb.execute(
  #       f"SELECT MAX(update_ts) as max_ts FROM bed_updates WHERE icu_id = {i}"
  #     )
  #     max_ts = res.iloc[0]["max_ts"]
  #     self.assertEqual(
  #       bedcount[bedcount["icu_id"] == i].iloc[0]["update_ts"], max_ts
  #     )

if __name__ == "__main__":
  absltest.main()
