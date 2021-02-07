import 'dart:convert';

import 'package:http/http.dart' as http;

const url = "";

Future<Map<String, dynamic>> simulateOrder() async {
  final response =
      await http.post(Uri.http(url, 'orders'), body: {'name': 'test'});
  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception("Failed to make request.");
  }
}

Future<Map<String, dynamic>> findOrder() async {
  final response =
      await http.post(Uri.http(url, 'orders/find'), body: {'name': 'test'});

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception("Failed to make request.");
  }
}
