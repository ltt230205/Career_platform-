// @ts-nocheck
db.test.insertMany([
  {
    name: "Test Document",
    value: 42,
    describe: "tung yeu",
    created_at: new Date()
  }
]);

print("=== SELECT RESULT ===");

db.test.find({ describe: "tung yeu" }).pretty();
