# Proje Açıklaması:
Proje, roboflow üzerinden veri setleri ile eğitilmiş modellerle sürücü yorgunluk tespiti üzerine yapılmış bir demodur.

Roboflow üzerinden farklı parametrelerle eğitilmiş modeller olsa da temelde iki adet model vardır. Bu modellerden biri göz takibi diğeri de eseneme takibi yapıyor. 

OpenCV ile gerçek zamanlı video akışı üzerinden sürücüde göz açık kapalılığı ve esneme durumu takip ediliyor. Şu an için bu demoda sadece göz takibi sırasında bir uyarı sistemi kullanılmıştır. 

Göz takibi için kullanılan uyarı sisteminde, belirli bir süre göz kapalı kalırsa alarm sesi ile sürücü uyarılıyor. Eğer bu durum birden çok kez tekrarlanırsa her defasında alarmla uyarılır ve sonrasnda flask ile açılan bir web sunucusuyla haberleşir. Bu sunucuyla haberleşme nedeni, google maps apisi kullanılarak konumun 5km çevresindeki, sürücünün dinlenebileceği en yakın 5 yerin listelenmesidir. Daha sonra yol tarifi al denildiğinde, seçilen konuma otomatik yol tarifnin başlatılmasıdır. 